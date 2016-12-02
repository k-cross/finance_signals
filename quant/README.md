Quant Approach
==============================

## Areas of Exploration

- Technicals
    + Basics
        * SMA crossovers, hitting 200 SMA
        * BBs: over/undersold, if it fits in a channel that's a good sign
    + Advanced
        * Finding support/resistance levels
        * Situational: upswing/downswing/going sideways
        * RSI: downswings and predicting rebounds
    + Moonshot
        * Trend lines and channels
        * Identify overshooting
        * Deviation from related companies and market index
- Assign importance to each indicator
    + i.e. BB might be more important than 200 SMA
    + Create your own neural net or perceptron, adding weights for final decision
- Associating "attributes" with companies
    + Level of earning report volatility
    + year on year growth
- Google Trends
- Apply machine learning?

## Plan of Action

1. ~~Time machine: **basic "controller" with Python** that executes prediction for specific time and gauges accuracy, provides predictor with only the data up to that point to simulate prediction done in the past~~
2. ~~Write prediction engine skeleton that **calculates technical indicators** for historical data~~
3. ~~Read data from historical prices and **generate prediction** using simple technicals and other indicators~~
4. ~~Controller checks prediction vs actual price, **scoots to next date** and calculates again, simulating passing of time, prediction accuracy does not matter yet~~
5. ~~**Run on entire historical data set** and see how it performs~~
6. **Assign weights** to individual indicators depending on likelihood, importance, etc and try to optimize prediction accuracy
7. Implement mapreduce by **distributing processing for historic data**
8. Try to implement **advanced technicals** and improve accuracy
9. Implement **Moonshot technicals**

## Instructions

### Installation

1. Install TA-lib libraries as per here: https://github.com/mrjbq7/ta-lib#installation
2. Install `matplotlib`, `tkinter`, `numpy` and `TA-lib` python packages with `pip3`, and any others that may be missing.
3. Ready to go!

### Running

Currently only with:
`python3 quantpredict.py`

Hopefully today's prediction will soon be:
`python3 quantpredict.py`

## Misc

AMZN chart for reference:
[2YR, Daily, 200 SMA, 100 BB](https://finance.yahoo.com/chart/AMZN#eyJzaG93QXJlYSI6ZmFsc2UsInNob3dMaW5lIjpmYWxzZSwibXVsdGlDb2xvckxpbmUiOmZhbHNlLCJzaG93T2hsYyI6dHJ1ZSwic2hvd0JvbGxpbmdlciI6dHJ1ZSwiYm9sbGluZ2VyVXBwZXJDb2xvciI6IiNlMjAwODEiLCJib2xsaW5nZXJMb3dlckNvbG9yIjoiIzk1NTJmZiIsImJvbGxpbmdlclBlcmlvZCI6MTAwLCJzaG93U21hIjp0cnVlLCJzbWFDb2xvcnMiOiIjMWFjNTY3Iiwic21hUGVyaW9kcyI6IjIwMCIsInNtYVdpZHRocyI6IjEiLCJzbWFHaG9zdGluZyI6IjAiLCJtZmlMaW5lQ29sb3IiOiIjNDVlM2ZmIiwibWFjZERpdmVyZ2VuY2VDb2xvciI6IiNmZjdiMTIiLCJtYWNkTWFjZENvbG9yIjoiIzc4N2Q4MiIsIm1hY2RTaWduYWxDb2xvciI6IiMwMDAwMDAiLCJyc2lMaW5lQ29sb3IiOiIjZmZiNzAwIiwic3RvY2hLTGluZUNvbG9yIjoiI2ZmYjcwMCIsInN0b2NoRExpbmVDb2xvciI6IiM0NWUzZmYiLCJsaW5lVHlwZSI6ImJhciIsInJhbmdlIjoiMnkifQ%3D%3D)
