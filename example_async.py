from igloo import Client, User
import asyncio
from random import randint


def read_temp():
    return randint(5, 25)


def read_humidity():
    return randint(30, 70)


async def monitor_temperature():
    while True:
        print("Temperature now: %d" % read_temp())
        await asyncio.sleep(1)


async def monitor_humidity():
    while True:
        print("Humidity now: %d" % read_humidity())
        await asyncio.sleep(1)


async def keepOnline(client):
    async for _ in client.subscription_root.keepOnline("39fc078e-a94d-4184-8008-3e97750f5e73"):
        pass


async def main():
    client = Client(asyncio=True, token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOiJmODFhODQ3Zi1mZDAyLTQzMDgtOWY3Zi02MTNkZjQ2OTUyNzMiLCJ0b2tlbklkIjoiZjdiZDA1NzMtZTYzMC00ZGIxLTllMTItODE2MDA5NTgyODU4IiwiYWNjZXNzTGV2ZWwiOiJERVZJQ0UiLCJ0b2tlblR5cGUiOiJQRVJNQU5FTlQifQ.VuPRvdMayBg7GxixT4QBjXd3jYO_3Q24Fctx508_p5iRxY96zv0z9-UXQsYGJiJjsI3E7ei2gtgEF84gsm8bnA")

    # print(await client.query_root.user.name)
    # async for device in client.subscription_root.deviceUpdated():
    #     print("{device} updated".format(device=await device.name))
    await asyncio.gather(monitor_humidity(), monitor_temperature(), keepOnline(client))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
