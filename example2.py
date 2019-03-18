import asyncio
import igloo
from igloo import User, Client

client = Client(token="")

# async def listen():
#     counter = 0
#     async for data in client.subscribe("subscription{ environmentCreated{ id }}"):
#         print(data)
#         counter = counter + 1
#         if counter > 3:
#             return

# asyncio.get_event_loop().run_until_complete(listen())

# creates an environment
# mutationRes = client.mutation(
#     'mutation{ createEnvironment(name:"AAAAAAA"){id}}')

# print(mutationRes)

# queryRes = client.query('query user($email: String){user(email:$email){name id}}', variables={
#                         "email": "andrea@igloo.ooo"})

# print(queryRes)

user = User(client)
user.name = "Igloo Test"
print(user.name)

for environment in user.environments:
    print(environment.name)
