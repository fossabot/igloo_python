class Device:
    def __init__(self, client, id):
        self.client = client
        self.id = id

    @property
    def deviceType(self):
        res = self.client.query('{device(id:"%s"){deviceType}}' %
                                self.id, keys=["device", "deviceType"])
        return res

    @deviceType.setter
    def deviceType(self, newDeviceType):
        self.client.mutation(
            'mutation{device(id:"%s", deviceType:"%s"){id}}' % (self.id, newDeviceType), asyncio=False)
