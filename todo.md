ToDo
==============================

## Areas of Exploration

- Technicals
    + Finding support/resistance levels
    + SMA crossovers
    + Calculating BBs
    + Recognize overshooting
    + Deviation from related companies and market index
- Monte Carlo method & standard deviation
- Associating "attributes" with companies
    + Level of earning report volatility
    + year on year growth
- Google Trends

## Plan of Action

- Create sample data set emulating price movement
    + Specially selected to test technical indicator detection
    + Basic "hello world" test
- Run on entire historical data
- Assign importance to each indicator
    + Refer to "Areas of Exploration" and "Outline"
    + Create your own neural net or perceptron, adding weights for final decision
- Apply though machine learning 

### Steps

1. **Basic "controller" with Python**: executes prediction for specific time and gauge accuracy, provides it only the data up to that point
2. Write prediction engine skeleton that **calculates technical indicators**
3. Read data from historical prices and **generate prediction**
4. Controller checks prediction accuracy, scoots to next date and calculates again

AMZN chart for reference:
[2YR, Daily, 200 SMA, 100 BB](https://finance.yahoo.com/chart/AMZN#eyJzaG93QXJlYSI6ZmFsc2UsInNob3dMaW5lIjpmYWxzZSwibXVsdGlDb2xvckxpbmUiOmZhbHNlLCJzaG93T2hsYyI6dHJ1ZSwic2hvd0JvbGxpbmdlciI6dHJ1ZSwiYm9sbGluZ2VyVXBwZXJDb2xvciI6IiNlMjAwODEiLCJib2xsaW5nZXJMb3dlckNvbG9yIjoiIzk1NTJmZiIsImJvbGxpbmdlclBlcmlvZCI6MTAwLCJzaG93U21hIjp0cnVlLCJzbWFDb2xvcnMiOiIjMWFjNTY3Iiwic21hUGVyaW9kcyI6IjIwMCIsInNtYVdpZHRocyI6IjEiLCJzbWFHaG9zdGluZyI6IjAiLCJtZmlMaW5lQ29sb3IiOiIjNDVlM2ZmIiwibWFjZERpdmVyZ2VuY2VDb2xvciI6IiNmZjdiMTIiLCJtYWNkTWFjZENvbG9yIjoiIzc4N2Q4MiIsIm1hY2RTaWduYWxDb2xvciI6IiMwMDAwMDAiLCJyc2lMaW5lQ29sb3IiOiIjZmZiNzAwIiwic3RvY2hLTGluZUNvbG9yIjoiI2ZmYjcwMCIsInN0b2NoRExpbmVDb2xvciI6IiM0NWUzZmYiLCJsaW5lVHlwZSI6ImJhciIsInJhbmdlIjoiMnkifQ%3D%3D)
