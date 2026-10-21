# -*- coding: utf-8 -*-
"""WebSocket 字幕服务: 向 Edge 插件/网页推送实时字幕。"""
import asyncio
import json

import websockets


class SubtitleServer:
    def __init__(self):
        self.clients = set()

    async def _handler(self, ws):
        self.clients.add(ws)
        try:
            async for _ in ws:
                pass
        finally:
            self.clients.discard(ws)

    async def _main(self, host, port):
        async with websockets.serve(self._handler, host, port):
            print(f"[server] WebSocket 字幕服务运行在 ws://{host}:{port}")
            await asyncio.Future()

    def run(self, host="127.0.0.1", port=8765):
        asyncio.run(self._main(host, port))

    def broadcast(self, data: dict):
        """同步广播给所有已连接客户端。"""
        msg = json.dumps(data, ensure_ascii=False)
        for ws in list(self.clients):
            try:
                asyncio.run_coroutine_threadsafe(ws.send(msg), ws.loop)
            except Exception:
                pass
