import asyncio
import igloo

client = igloo.Client(username="andrea@igloo.ooo",
                      password="sleeping polar bear")


async def listen():
    counter = 0
    async for data in client.subscribe("subscription{ environmentCreated{ id }}"):
        print(data)
        counter = counter + 1
        if counter > 3:
            return

asyncio.get_event_loop().run_until_complete(listen())

# creates an environment
mutationRes = client.mutation(
    'mutation{ createEnvironment(name:"AAAAAAA"){id}}')

print(mutationRes)
