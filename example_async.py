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
    async for data in client.subscription_root.deviceUpdated():
        print(data)


async def main():
    client = Client(asyncio=True, token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOiJlNzYxZmZlMi1lM2Q5LTQ0YjYtYjYyZC00M2Y4ZTljMTRjNjIiLCJ0b2tlbklkIjoiMGQxNTcxNGEtM2UyZS00NjFhLTg2ZTMtOGQwZWUwMTY4NWEzIiwiYWNjZXNzTGV2ZWwiOiJERVZJQ0UiLCJ0b2tlblR5cGUiOiJQRVJNQU5FTlQifQ.ttiW6TVvcKoWmhDSL8fTqq_ItWvPa_41zolI4gRi2zwKlUVV-PWRMk3QM1ZcAuEuOtGGLaPuilR-4Z6JZf13ag")

    async for i in client.subscription_root.deviceUpdated():
        pass
    # await asyncio.gather(monitor_humidity(), monitor_temperature(), client.subscription_root.keepOnline("229718d6-e4fe-43dd-a2e6-6504a2e9a5f9"))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
