
from aiodataloader import DataLoader


class DeviceLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{device(id:"%s"){%s}}' % (self._id, fields), keys=["device"])

        resolvedValues = [res[key] for key in keys]

        return resolvedValues


class Device:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = DeviceLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def deviceType(self):
        if self.client.asyncio:
            return self.loader.load("deviceType")
        else:
            return self.client.query('{device(id:"%s"){deviceType}}' %
                                     self._id, keys=["device", "deviceType"])

    @deviceType.setter
    def deviceType(self, newDeviceType):
        self.client.mutation(
            'mutation{device(id:"%s", deviceType:"%s"){id}}' % (self._id, newDeviceType), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{device(id:"%s"){myRole}}' %
                                     self._id, keys=["device", "myRole"])

    @property
    def starred(self):
        if self.client.asyncio:
            return self.loader.load("starred")
        else:
            return self.client.query('{device(id:"%s"){starred}}' %
                                     self._id, keys=["device", "starred"])

    @starred.setter
    def starred(self, newValue):
        self.client.mutation(
            'mutation{device(id:"%s", starred:%s){id}}' % (self._id, "true" if newValue else "false"), asyncio=False)

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{device(id:"%s"){name}}' %
                                     self._id, keys=["device", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{device(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{device(id:"%s"){index}}' %
                                     self._id, keys=["device", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{device(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def online(self):
        if self.client.asyncio:
            return self.loader.load("online")
        else:
            return self.client.query('{device(id:"%s"){online}}' %
                                     self._id, keys=["device", "online"])

    @property
    def storageUsed(self):
        if self.client.asyncio:
            return self.loader.load("storageUsed")
        else:
            return self.client.query('{device(id:"%s"){storageUsed}}' %
                                     self._id, keys=["device", "storageUsed"])

    @property
    def signalStatus(self):
        if self.client.asyncio:
            return self.loader.load("signalStatus")
        else:
            return self.client.query('{device(id:"%s"){signalStatus}}' %
                                     self._id, keys=["device", "signalStatus"])

    @signalStatus.setter
    def signalStatus(self, newValue):
        self.client.mutation(
            'mutation{device(id:"%s", signalStatus:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def batteryStatus(self):
        if self.client.asyncio:
            return self.loader.load("batteryStatus")
        else:
            return self.client.query('{device(id:"%s"){batteryStatus}}' %
                                     self._id, keys=["device", "batteryStatus"])

    @batteryStatus.setter
    def batteryStatus(self, newValue):
        self.client.mutation(
            'mutation{device(id:"%s", batteryStatus:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def batteryCharging(self):
        if self.client.asyncio:
            return self.loader.load("batteryCharging")
        else:
            return self.client.query('{device(id:"%s"){batteryCharging}}' %
                                     self._id, keys=["device", "batteryCharging"])

    @batteryCharging.setter
    def batteryCharging(self, newValue):
        self.client.mutation(
            'mutation{device(id:"%s", batteryCharging:%s){id}}' % (self._id, "true" if newValue else "false"), asyncio=False)

    @property
    def firmware(self):
        if self.client.asyncio:
            return self.loader.load("firmware")
        else:
            return self.client.query('{device(id:"%s"){firmware}}' %
                                     self._id, keys=["device", "firmware"])

    @firmware.setter
    def firmware(self, newValue):
        self.client.mutation(
            'mutation{device(id:"%s", firmware:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def muted(self):
        if self.client.asyncio:
            return self.loader.load("muted")
        else:
            return self.client.query('{device(id:"%s"){muted}}' %
                                     self._id, keys=["device", "muted"])

    @muted.setter
    def muted(self, newValue):
        self.client.mutation(
            'mutation{device(id:"%s", muted:%s){id}}' % (self._id, "true" if newValue else "false"), asyncio=False)

    @property
    def qrCode(self):
        if self.client.asyncio:
            return self.loader.load("qrCode")
        else:
            return self.client.query('{device(id:"%s"){qrCode}}' %
                                     self._id, keys=["device", "qrCode"])
