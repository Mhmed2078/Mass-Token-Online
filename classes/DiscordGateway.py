import asyncio
import websockets
import json
from aioconsole import aprint
import time


class discordgateway:
    def __init__(self, token: str) -> None:
        self.token = token



    async def recv_json(self):
        item = await self.ws.recv()
        return json.loads(item)

    async def send_json(self, payload: dict):
        await self.ws.send(json.dumps(payload))

    async def simple_connect(self):
        await self.connect()
        interval = await self.recv_json()
        await self.identify()
        asyncio.create_task(self.heartbeat(interval['d']['heartbeat_interval'] / 1000))
        event = await self.recv_json()
        if event["t"] == "READY":
            await aprint(f"CONNECTED AS: {event['d']['user']['username']}#{event['d']['user']['discriminator']}")
        await self.begin_presence()
        while True:
            event = await self.recv_json()
            await aprint(event["t"])

    async def connect(self):
        self.ws = await websockets.connect("wss://gateway.discord.gg/?encoding=json&v=9")

    async def identify(self):
        payload = {
            'op': 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "android",
                    "$browser": "Discord Android",
                    "$device": "Discord Android",
                    '$referrer': "",
                    '$referring_domain': ""
                },

            }
        }

        await self.send_json(payload)



    async def heartbeat(self, interval):
        await aprint(f"Hearbeat loop has began with the interval of {interval} seconds!")
        heartbeatJSON = {
            "op": 1,
            "d": time.time()
        }
        while True:
            await asyncio.sleep(interval)
            await self.send_json(heartbeatJSON)
            await aprint("Sent BEAT")

    async def begin_presence(self):
        payload = {
            "op": 3,
            "d": {
                "since": time.time(),
                "activities": [{
                    "name": "𝗢𝗠𝗘𝗚𝗔",
                    # "state": "Too alpha halal male",
                    "type": 3,
                    "application_id": "971441537781223435",
                    "created_at": time.time(),
                    "since": 0,
                    # "details": "Being Alpha Halal Male",
                    "assets": {
                        "large_image":"976840462952460288",
                        "large_text":"𝗢𝗠𝗘𝗚𝗔"
                    },
                    "buttons":["JOIN OMEGA"],
                    "metadata":{
                        "button_urls":["https://discord.gg/ZRw9ATstkB"]
                    },
                }],
                "status": "online",
                "afk": False,
            }
        }
        await self.send_json(payload)