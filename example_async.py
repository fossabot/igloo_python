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
    client = Client(asyncio=True, token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOiJmMTAyZGVhYy0wZGQyLTQwZWQtOTM4NS1lMzI3YjM0M2Y2ZmUiLCJ0b2tlbklkIjoiYWRjMjg4MzgtOGUyMi00OWYyLWI1ZDktYWI4M2Y0M2ZkN2RkIiwiYWNjZXNzTGV2ZWwiOiJERVZJQ0UiLCJ0b2tlblR5cGUiOiJQRVJNQU5FTlQifQ.f7GWid4sS8GhQB_qb9PQlI98ULp3HC3-63Ja97vuLYcFCzg9vKF-P5b1GBCgh1t_2GD3qa2p_UeIF5y6Ues65g")

    # await asyncio.gather(monitor_humidity(), monitor_temperature(), client.subscription_root.keepOnline("229718d6-e4fe-43dd-a2e6-6504a2e9a5f9"))
    await asyncio.gather(monitor_humidity(), monitor_temperature(), keepOnline(client))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
