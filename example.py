from igloo import Client

client = Client(token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOiJmMTAyZGVhYy0wZGQyLTQwZWQtOTM4NS1lMzI3YjM0M2Y2ZmUiLCJ0b2tlbklkIjoiYWRjMjg4MzgtOGUyMi00OWYyLWI1ZDktYWI4M2Y0M2ZkN2RkIiwiYWNjZXNzTGV2ZWwiOiJERVZJQ0UiLCJ0b2tlblR5cGUiOiJQRVJNQU5FTlQifQ.f7GWid4sS8GhQB_qb9PQlI98ULp3HC3-63Ja97vuLYcFCzg9vKF-P5b1GBCgh1t_2GD3qa2p_UeIF5y6Ues65g")

# user = client.query_root.user
# user.name = "Andrea"

# print("Here are the first 3 environments of user {}".format(user.name))
# for environment in user.environments[:3]:
#     print("- {} ({})".format(environment.name, len(environment.devices)))
#     for device in environment.devices:
#         print("  - {}".format(device.name))

print(client.mutation_root.verifyPassword(
    "andrea@igloo.ooo", "sleeping polar bear"))

# OUTPUT:
# Here are the first 3 environments of user Andrea
# - A (0)
# - A (1)
#   - Claimed device
# - A (0)
