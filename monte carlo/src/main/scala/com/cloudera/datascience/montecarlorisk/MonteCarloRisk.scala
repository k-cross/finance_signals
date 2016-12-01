package com.cloudera.datascience.montecarlorisk

import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.serializer.{KryoSerializer, KryoRegistrator}
import com.esotericsoftware.kryo.Kryo
import org.apache.commons.math3.random.MersenneTwister
import org.apache.commons.math3.distribution.MultivariateNormalDistribution
import org.apache.commons.math3.stat.correlation.Covariance
import org.apache.commons.math3.stat.regression.OLSMultipleLinearRegression

import scala.io.Source
import scala.collection.mutable.ArrayBuffer
import java.text.SimpleDateFormat
import java.io.File
import java.io.PrintWriter

case class Instrument(factorWeights: Array[Double], minValue: Double = 0,
  maxValue: Double = Double.MaxValue)

class MyRegistrator extends KryoRegistrator {
  override def registerClasses(kryo: Kryo) {
    kryo.register(classOf[Instrument])
  }
}

object MonteCarloRisk {
  def main(args: Array[String]) {
    val sparkConf = new SparkConf().setAppName("Monte Carlo Risk (VaR) Computer")
    sparkConf.set("spark.serializer", classOf[KryoSerializer].getName)
    sparkConf.set("spark.kryo.registrator", classOf[MyRegistrator].getName)
    val sc = new SparkContext(sparkConf)

    // Parse arguments and read input data
    val instruments = readInstruments(args(0))
    val numTrials = 10000000
    val parallelism = 1000
    val factorMeans = readMeans(args(3))
    val factorCovariances = readCovariances(args(4))
    val seed = if (args.length > 5) args(5).toLong else System.currentTimeMillis()

    // Additions to Instruments
    val start = new DateTime(2010, 07, 1, 0, 0)
    val end = new DateTime(2015, 05, 1, 0, 0)
    
    val files = new File("data/stocks/").listFiles()
    val rawStocks: Seq[Array[(DateTime, Double)]] =
      files.flatMap(file => {
        try {
          Some(readYahooHistory(file))
        }
        catch {
          case e: Exception => None
        }
      }).filter(_.size >= 260*5)
    
    val stocks: Seq[Array[Double]] = rawStocks.
      map(trimToRegion(_, start, end)).
      map(fillInHistory(_, start, end))
    
    val stocksReturns = stocks.map(twoWeekReturns)
    val factorsReturns = factors.map(twoWeekReturns)
    val factorMat = factorMatrix(factorsReturns)
    val factorFeatures = factorMat.map(featurize)
    val models = stocksReturns.map(linearModel(_, factorFeatures))
    val factorWeights = models.map(_.estimateRegressionParameters()).toArray


    // Send all instruments to every node
    val broadcastInstruments = sc.broadcast(instruments)

    // Generate different seeds so that our simulations don't all end up with the same results
    val seeds = (seed until seed + parallelism)
    val seedRdd = sc.parallelize(seeds, parallelism)

    // Main computation: run simulations and compute aggregate return for each
    val trialsRdd = seedRdd.flatMap(trialValues(_, numTrials / parallelism,
      broadcastInstruments.value, factorMeans, factorCovariances))

    // Cache the results so that we don't recompute for both of the summarizations below
    trialsRdd.cache()

    // Calculate VaR
    val varFivePercent = trialsRdd.takeOrdered(math.max(numTrials / 20, 1)).last
    println("VaR: " + varFivePercent)

    // Kernel density estimation
    val domain = Range.Double(20.0, 60.0, .2).toArray
    val densities = KernelDensity.estimate(trialsRdd, 0.25, domain)
    val pw = new PrintWriter("densities.csv")
    for (point <- domain.zip(densities)) {
      pw.println(point._1 + "," + point._2)
    }
    pw.close()
  }

  def trialValues(seed: Long, numTrials: Int, instruments: Seq[Instrument],
      factorMeans: Array[Double], factorCovariances: Array[Array[Double]]): Seq[Double] = {
    val rand = new MersenneTwister(seed)
    val multivariateNormal = new MultivariateNormalDistribution(rand, factorMeans,
      factorCovariances)

    val trialValues = new Array[Double](numTrials)
    for (i <- 0 until numTrials) {
      val trial = multivariateNormal.sample()
      trialValues(i) = trialValue(trial, instruments)
    }
    trialValues
  }

  /**
   * Calculate the full value of the portfolio under particular trial conditions.
   */
  def trialValue(trial: Array[Double], instruments: Seq[Instrument]): Double = {
    var totalValue = 0.0
    for (instrument <- instruments) {
      totalValue += instrumentTrialValue(instrument, trial)
    }
    totalValue
  }

  /**
   * Calculate the value of a particular instrument under particular trial conditions.
   */
  def instrumentTrialValue(instrument: Instrument, trial: Array[Double]): Double = {
    var instrumentTrialValue = 0.0
    var i = 0
    while (i < trial.length) {
      instrumentTrialValue += trial(i) * instrument.factorWeights(i)
      i += 1
    }
    Math.min(Math.max(instrumentTrialValue, instrument.minValue), instrument.maxValue)
  }

  def readInstruments(instrumentsFile: String): Array[Instrument] = {
    val src = Source.fromFile(instrumentsFile)
    // First and second elements are the min and max values for the instrument
    val instruments = src.getLines().map(_.split(",")).map(
      x => new Instrument(x.slice(2, x.length).map(_.toDouble), x(0).toDouble, x(1).toDouble))
    instruments.toArray
  }

  def readMeans(meansFile: String): Array[Double] = {
    val src = Source.fromFile(meansFile)
    val means = src.getLines().map(_.toDouble)
    means.toArray
  }

  def readCovariances(covsFile: String): Array[Array[Double]] = {
    val src = Source.fromFile(covsFile)
    val covs = src.getLines().map(_.split(",")).map(_.map(_.toDouble))
    covs.toArray
  }

  def readYahooHistory(file: File): 
    Array[(DateTime, Double)] = {
      val format = new SimpleDateFormat("yyyy-MM-dd")
      val lines = Source.fromFile(file).getLines().toSeq
      lines.tail.map(line => {
        val cols = line.split(',')
        val date = new DateTime(format.parse(cols(0)))
        val value = cols(1).toDouble
        (date, value)
      }).reverse.toArray
  }

  def trimToRegion(history: Array[(DateTime, Double)],
                   start: DateTime,
                   end: DateTime):
    Array[(DateTime, Double)] = {
    var trimmed = history.
      dropWhile(_._1 < start).takeWhile(_._1 <= end)
    if (trimmed.head._1 != start) {
      trimmed = Array((start, trimmed.head._2)) ++ trimmed
    }
    if (trimmed.last._1 != end) {
      trimmed = trimmed ++ Array((end, trimmed.last._2))
    }
    trimmed
  }

  def fillInHistory(history: Array[(DateTime, Double)],
                    start: DateTime,
                    end: DateTime):
    Array[(DateTime, Double)] = {
      var cur = history
      val filled = new ArrayBuffer[(DateTime, Double)]()
      var curDate = start
  
      while (curDate < end) {
        if (cur.tail.nonEmpty && cur.tail.head._1 == curDate) {
          cur = cur.tail
        }
  
        filled += ((curDate, cur.head._2))
  
        curDate += 1.days
        // Skip weekends
        if (curDate.dayOfWeek().get > 5) curDate += 2.days
      }
      filled.toArray
  }
  
  def twoWeekReturns(history: Array[(DateTime, Double)]):
    Array[Double] = {
      history.sliding(10).
        map(window => window.last._2 - window.head._2).toArray
  }
  
  def factorMatrix(histories: Seq[Array[Double]]):
    Array[Array[Double]] = {
      val mat = new Array[Array[Double]](histories.head.length)
      for (i <- 0 until histories.head.length) {
        mat(i) = histories.map(_(i)).toArray
      }
      mat
  }
}
