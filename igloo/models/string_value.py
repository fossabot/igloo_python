
from aiodataloader import DataLoader
from .device import Device


class StringValueLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{stringValue(id:"%s"){%s}}' % (self._id, fields), keys=["stringValue"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching device{id} the result is in the device key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class StringValue:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = StringValueLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{stringValue(id:"%s"){name}}' % self._id, keys=[
                "stringValue", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{stringValue(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def visibility(self):
        if self.client.asyncio:
            return self.loader.load("visibility")
        else:
            return self.client.query('{stringValue(id:"%s"){visibility}}' % self._id, keys=[
                "stringValue", "visibility"])

    @visibility.setter
    def visibility(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", visibility:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def cardSize(self):
        if self.client.asyncio:
            return self.loader.load("cardSize")
        else:
            return self.client.query('{stringValue(id:"%s"){cardSize}}' % self._id, keys=[
                "stringValue", "cardSize"])

    @cardSize.setter
    def cardSize(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", cardSize:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{stringValue(id:"%s"){index}}' % self._id, keys=[
                "stringValue", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{stringValue(id:"%s"){myRole}}' % self._id, keys=[
                "stringValue", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{stringValue(id:"%s"){createdAt}}' % self._id, keys=[
                "stringValue", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{stringValue(id:"%s"){updatedAt}}' % self._id, keys=[
                "stringValue", "updatedAt"])

    async def _async_load_device(self):
        id = await self.loader.load("device{id}")["id"]
        return Device(self.client, id)

    @property
    def device(self):
        if self.client.asyncio:
            return self._async_load_device()
        else:
            id = self.client.query('{stringValue(id:"%s"){device{id}}}' % self._id, keys=[
                "stringValue", "device", "id"])

            return Device(self.client, id)
