Financial Signals Analysis
==============================

## Setup and Installation

* From sandbox grab two other dependencies for the E-Trade API
    * `xstream`
    * `commons-httpclient-contrib-ssl`

## Scope and Approach

* Using the Monte-Carlo method to analyze risk for the equities markets.
    * Limits range to two sigma to bound the range of possibility within a given certainty for the model.
    * Might try to use other optimization factors and methods.
* Currently focused on the technologies industries.

## Tickers

Using one to two of the largest in each industry subset with a few exceptions.

| Ticker | Industry          |
| ------ | ----------------- |
| AMZN   | Internet Services |
| GOOGL  | Internet Services |
| FB     | Internet Services |
| AAPL   | Consumer Goods    |
| MSFT   | Business Software |
| IBM    | Business Software |
| ORCL   | Business Software |

## Outline

> Using historical data try to predict how the stock will move in the future

- Given a ticker/company, analyze historical data and predict movement using relevant factors
- Potential factors to consider:
    + Global events
    + Political events
    + Foreign affairs
    + Quarterly reports
    + Fed Meetings, rate hike, etc.
    + Deviation from indexes or tickers in same industry
- Aiming for long term trading, profitability in weeks/months timeframe

## Decide if

- Are we predicting stocks of a specific industry?
    + They all react different amounts to different factors
    + Tech, finance, retail, natural resource, etc.
