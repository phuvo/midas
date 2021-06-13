# Midas

Midas is a cryptocurrency options trading framework written in Python. It supports both backtesting and live trading.

## Supported exchanges

At the moment Midas only supports [Deribit](https://www.deribit.com/).

## Historical data

You will need the following data to backtest your strategies:
- Options (creation & expiration date)
- Tickers (best bid & ask price)
- Delivery prices

The `example` directory contains one week of data for BTC and ETH daily options on Deribit. Ticker data were recorded every 15 minutes.
