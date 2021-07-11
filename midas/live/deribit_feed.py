from __future__ import annotations
from typing import Any

from aiohttp_rpc import WsJsonRpcClient
from midas.base.feed import DataFeed, OnMessage, Option
from midas.helpers.datetime import from_ms
from midas.types.ticker import create_ticker


class DeribitFeed(DataFeed):
    def __init__(self, ws_url: str):
        """Use `DeribitFeed.create` to create an instance of this class."""
        self._ws = WsJsonRpcClient(ws_url, json_request_handler=self._on_request)


    @staticmethod
    async def create(ws_url: str):
        feed = DeribitFeed(ws_url)
        await feed._ws.connect()
        return feed


    async def get_options(self, currency: str, expired: bool = False):
        raw_options = await self._ws.call(
            'public/get_instruments', currency=currency, expired=expired, kind='option',
        )
        all_options = [create_option(item) for item in raw_options]
        return sorted(all_options, key=lambda option: (option.expiration, option.strike))


    async def subscribe(self, channels: list[str], on_message: OnMessage):
        self._on_message = on_message
        await self._ws.call('public/subscribe', channels=channels)


    async def _on_request(self, json_request: dict[str, Any], **kwargs: list[Any]):
        self._on_message(json_request)


    async def get_ticker(self, instrument: str):
        ticker = await self._ws.call('public/ticker', instrument_name=instrument)
        return create_ticker(ticker)


def create_option(item: dict[str, Any]):
    return Option(
        name      =item['instrument_name'],
        creation  =from_ms(item['creation_timestamp']),
        expiration=from_ms(item['expiration_timestamp']),
        strike    =int(item['strike']),
        type      =item['option_type'],
    )
