from igloo import User, Client

client = Client(token="")

user = User(client)
user.name = "Andrea"

print("Here are the first 3 environments of user "+user.name)
for environment in user.environments[:3]:
    print("- {} ({})".format(environment.name, len(environment.devices)))
    for device in environment.devices:
        print("  - {}".format(device.name))

# OUTPUT:
# Here are the first 3 environments of user Andrea
# - A (0)
# - A (1)
#   - Claimed device
# - A (0)
