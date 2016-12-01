import com.github.nscala_time.time.Imports._
import com.cloudera.datascience.risk.KernelDensity
import org.apache.commons.math3.distribution.MultivariateNormalDistribution
import org.apache.commons.math3.stat.regression.OLSMultipleLinearRegression
import org.apache.commons.math3.stat.correlation.PearsonsCorrelation
import org.apache.commons.math3.stat.correlation.Covariance
import org.apache.commit.math3.random.MersenneTwister
import breeze.plot.
import java.text.SimpleDateFormat
import java.io.File
import scala.collection.mutable.ArrayBuffer
import scala.io.Source


def readHistoricalStockData(file: File):
  Array[(DateTime, Double)] = {
    val format = new SimpleDateFormat("yyyy-M-d")
    val lines = Source.fromFile(file).getLines().toSeq
    lines.map(line => {
      val cols = line.split(',')
      val date = new DateTime(format.parse(cols(0)))
      val value = cols(1).toDouble
      (date, value)
    }).reverse.toArray
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


def featurize(factorReturns: Array[Double]):
  Array[Double] = {
    val squaredReturns = factorReturns.
      map(x => math.signum(x) * x * x)
    val squaredRootedReturns = factorReturns.
      map(x => signum(x) * math.sqrt(math.abs(x)))
    squaredReturns ++ squaredRootedReturns ++ factorReturns
}


def linearModel(instrument: Array[Double], factorMatrix: Array[Array[Double]]):
  OLSMultipleLinearRegression = {
    val regression = new OLSMultipleLinearRegression()
    regression.newSampleData(instrument, factorMatrix)
    regression
}


def plotDistribution(samples: Array[Double]) {
  val min = samples.min
  val max = samples.max
  val domain = Range.Double(min, max, (max - min) / 100).toList.toArray
  val densities = KernelDensity.estimate(samples, domain)
  val f = Figure()
  val p = f.subplot(0)

  p += plot(domain, densities)
  p.xlabel = "Two Week Return ($)"
  p.ylabel = "Density"
}


def instrumentTrialReturn(instrument: Array[Double], trial: Array[Double]):
  Double = {
    var instrumentTrialReturn = instrument(0)
    var i = 0
    while (i < trial.length) {
      instrumentTrialReturn += trial(i) * instrument(i+1)
      i += 1
    }
    instrumentTrialReturn
}


def trialReturn(trial: Array[Double], instruments: Seq[Array[Double]]): 
  Double = {
    var totalReturn = 0.0
    for (instrument <- instruments) {
      totalReturn += instrumentTrialReturn(instrument, trial)
    }
    totalReturn
}


def trialReturns(seed: Long, numTrials: Int, instruments: Seq[Array[Double]],
  factorMeans: Array[Double], factorCovariances: Array[Array[Double]]):
  Seq[Double] = {
    val rand = new MersenneTwister(seed)
    val multivariateNormal = new MultivariateNormalDistribution(
      rand, factorMeans, factorCovariances)
    val trialReturns = new Array[Double](numTrials)
    for (i <- 0 until numTrials) {
      val trialFactorReturns = multivariateNormal.sample()
      val trialFeatures = featurize(trialFactorReturns)
      trialReturns(i) = trialReturn(trialFeatures, instruments)
    }
    trialReturns
}


def fivePercentVaR(trials: RDD[Double]): Double = {
  val topLosses = trials.takeOrdered(math.max(trials.count().toInt / 20, 1))
  topLosses.last
}


def fivePercentCVaR(trials: RDD[Double]): Double = {
  val topLosses = trials.takeOrdered(math.max(trials.count().toInt / 20, 1))
  topLosses.sum / topLosses.length
}

val start = new DateTime(2010, 07, 1, 0, 0)
val end = new DateTime(2015, 05, 1, 0, 0)

val files = new File("history/stocks/").listFiles()
val rawStocks: Seq[Array[(DateTime, Double)]] =
  files.flatMap(file => {
    try {
      Some(readYahooHistory(file))
    }
    catch {
      case e: Exception => None
    }
  }).filter(_.size >= 260*5)

val factorsPrefix = "data/factors/"
val factors: Seq[Array[(DateTime, Double)]] =
  Array("SNP.csv", "NDX.csv").
  map(x => new File(factorsPrefix + x)).
  map(readYahooHistory)

val stocks: Seq[Array[Double]] = rawStocks.
  map(trimToRegion(_, start, end)).
  map(fillInHistory(_, start, end))

val stocksReturns = stocks.map(twoWeekReturns)
val factorsReturns = factors.map(twoWeekReturns)
val factorMat = factorMatrix(factorsReturns)
val factorFeatures = factorMat.map(featurize)
val models = stocksReturns.map(linearModel(_, factorFeatures))
val factorWeights = models.map(_.estimateRegressionParameters()).toArray

plotDistribution(factorsReturns(0))
plotDistribution(factorsReturns(1))

val factorCor = new PearsonsCorrelation(factorMat).
  getCorrelationMatrix().getData()

println(factorCor.map(_.mkString("\t")).mkString("\n"))

val factorCov = new Covariance(factorMat).getCovarianceMatrix().getData()
val factorMeans = factorsReturns.map(factor => factor.sum / factor.size).toArray
val factorsDist = new MultivariateNormalDistribution(factorMeans, factorCov)

factorsDist.sample() // Samples a set of market conditions

val parallelism = 1000
val baseSeed = 1496
val seeds = (baseSeed until baseSeed + parallelism)
val seedRdd = sc.parallelize(seeds, parallelism)
val numTrials = 10000000
val bFactorWeights = sc.broadcast(factorWeights)
val trials = seedRdd.flatMap(trialReturns(_, numTrials / parallelism,
  bFactorWeights.value, factorMeans, factorCov))
val valueAtRisk = fivePercentVaR(trials)
val conditionalValueAtRisk = fivePercentCVaR(trials)
