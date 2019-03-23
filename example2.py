import asyncio
import igloo
from igloo import User, Client

client = Client(token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOiJmMTAyZGVhYy0wZGQyLTQwZWQtOTM4NS1lMzI3YjM0M2Y2ZmUiLCJ0b2tlbklkIjoiYWRjMjg4MzgtOGUyMi00OWYyLWI1ZDktYWI4M2Y0M2ZkN2RkIiwiYWNjZXNzTGV2ZWwiOiJERVZJQ0UiLCJ0b2tlblR5cGUiOiJQRVJNQU5FTlQifQ.f7GWid4sS8GhQB_qb9PQlI98ULp3HC3-63Ja97vuLYcFCzg9vKF-P5b1GBCgh1t_2GD3qa2p_UeIF5y6Ues65g")

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
