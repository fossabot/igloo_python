class SubscriptionRoot:
    def __init__(self, client):
        self.client = client

    async def keepOnline(self, deviceId):
        async for _ in self.client.subscribe('subscription{keepOnline(deviceId:"%s")}' % deviceId):
            pass

    async def deviceUpdated(self):
        async for data in self.client.subscribe('subscription{deviceUpdated{id}}'):
            yield data

    async def valueUpdated(self):
        async for data in self.client.subscribe('subscription{valueUpdated{id}}'):
            yield data
