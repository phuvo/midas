from __future__ import annotations
from datetime import timedelta
from pathlib import Path
from typing import Any

import pandas
from pandas import DataFrame

from midas.base.feed import DataFeed, OnMessage, Option
from midas.base.ticker import Ticker
from midas.base.timer import Timer
from midas.helpers.datetime import from_ms


class CsvFeed(DataFeed):
    def __init__(self, timer: Timer):
        self._timer = timer


    def load_options(self, csv_files: list[str | Path]):
        options_lists = [read_options(str(file_path)) for file_path in csv_files]
        self._options = sum(options_lists, [])


    def load_tickers(self, csv_files: list[str | Path]):
        all_tickers = [read_tickers(str(file_path)) for file_path in csv_files]
        instruments = pandas.concat(all_tickers).groupby('instrument')

        tickers: dict[str, DataFrame] = {}
        for name, df in instruments:
            tickers[name] = df.set_index('timestamp')
        self._tickers = tickers


    async def get_options(self, currency: str, expired: bool = False):
        all_options = [option for option in self._options if option.name.startswith(currency)]
        today = self._timer.now()

        if expired:
            yesterday = today - timedelta(days=1)
            matches = [option for option in all_options if yesterday < option.expiration < today]
        else:
            matches = [option for option in all_options if option.creation < today < option.expiration]
        return sorted(matches, key=lambda option: (option.expiration, option.strike))


    async def subscribe(self, channels: list[str], on_message: OnMessage) -> None:
        raise NotImplementedError


    async def get_ticker(self, instrument: str):
        timestamp = int(self._timer.get_time() * 1000)
        frame = self._tickers[instrument]
        index: int = frame.index.get_loc(timestamp, method='pad')
        row = frame.iloc[index]
        return _create_ticker(row)


def snake_case(value: str):
    return value.lower().replace(' ', '_')


def read_options(file_path: str):
    df = pandas.read_csv(file_path)
    df.rename(columns=snake_case, inplace=True)
    return [create_option(item) for item in df.to_dict('records')]


def create_option(item: dict[str, Any]):
    parts = item['name'].split('-')
    return Option(
        name      =item['name'],
        creation  =from_ms(item['creation']),
        expiration=from_ms(item['expiration']),
        strike    =int(parts[2]),
        type      ='call' if parts[3] == 'C' else 'put',
    )


def read_tickers(file_path: str):
    df = pandas.read_csv(file_path)
    df.rename(columns=snake_case, inplace=True)
    return df


def _create_ticker(row: Any):
    return Ticker(
        instrument=row.instrument,
        timestamp =from_ms(row.name),
        bid_price =row.bid_price,
        mark_price=row.mark_price,
        ask_price =row.ask_price,
        underlying_price=row.underlying_price,
    )
