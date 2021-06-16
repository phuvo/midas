from __future__ import annotations
from typing import Any

from aiohttp_rpc import WsJsonRpcClient
from midas.base.feed import DataFeed


class DeribitFeed(DataFeed):
    def __init__(self, ws_url: str):
        """Use `DeribitFeed.create` to create an instance of this class."""
        self._ws = WsJsonRpcClient(ws_url, json_request_handler=self._on_request)


    @staticmethod
    async def create(config: dict[str, str]):
        feed = DeribitFeed(config['ws_url'])
        await feed._ws.connect()
        return feed


    async def get_options(self, currency: str, expired: bool = False):
        options = await self._ws.call(
            'public/get_instruments', currency=currency, expired=expired, kind='option',
        )
        return options


    async def subscribe(self, channels: list[str]):
        pass


    async def _on_request(self, json_request: dict[str, Any], **kwargs: list[Any]):
        pass
