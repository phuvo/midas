# Midas [![CI build](https://github.com/phuvo/midas/actions/workflows/ci-build.yml/badge.svg)](https://github.com/phuvo/midas/actions/workflows/ci-build.yml)

Midas is a cryptocurrency options trading framework written in Python. It supports both backtesting and live trading.

## Supported exchanges

At the moment Midas only supports [Deribit](https://www.deribit.com/).

## Historical data

You will need the following data to backtest your strategies:
- Options (creation & expiration date)
- Tickers (best bid & ask price)
- Delivery prices

The `example` directory contains one week of data for BTC options on Deribit. Ticker data were recorded every 30 minutes.

Use [get_delivery_prices](https://www.deribit.com/api/v2/public/get_delivery_prices?index_name=btc_usd&offset=0&count=10) endpoint to get delivery prices for BTC and ETH options.

## Quick start

```sh
$ poetry install
$ poetry run backtest
```

## Live trading

```sh
$ poetry run trade
```
