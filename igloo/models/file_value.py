
from aiodataloader import DataLoader


class FileValueLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{fileValue(id:"%s"){%s}}' % (self._id, fields), keys=["fileValue"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching device{id} the result is in the device key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class FileValue:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = FileValueLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{fileValue(id:"%s"){name}}' % self._id, keys=[
                "fileValue", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{fileValue(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def visibility(self):
        if self.client.asyncio:
            return self.loader.load("visibility")
        else:
            return self.client.query('{fileValue(id:"%s"){visibility}}' % self._id, keys=[
                "fileValue", "visibility"])

    @visibility.setter
    def visibility(self, newValue):
        self.client.mutation(
            'mutation{fileValue(id:"%s", visibility:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def cardSize(self):
        if self.client.asyncio:
            return self.loader.load("cardSize")
        else:
            return self.client.query('{fileValue(id:"%s"){cardSize}}' % self._id, keys=[
                "fileValue", "cardSize"])

    @cardSize.setter
    def cardSize(self, newValue):
        self.client.mutation(
            'mutation{fileValue(id:"%s", cardSize:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{fileValue(id:"%s"){index}}' % self._id, keys=[
                "fileValue", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{fileValue(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{fileValue(id:"%s"){myRole}}' % self._id, keys=[
                "fileValue", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{fileValue(id:"%s"){createdAt}}' % self._id, keys=[
                "fileValue", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{fileValue(id:"%s"){updatedAt}}' % self._id, keys=[
                "fileValue", "updatedAt"])

    async def _async_load_device(self):
        id = await self.loader.load("device{id}")["id"]

        from .device import Device
        return Device(self.client, id)

    @property
    def device(self):
        if self.client.asyncio:
            return self._async_load_device()
        else:
            id = self.client.query('{fileValue(id:"%s"){device{id}}}' % self._id, keys=[
                "fileValue", "device", "id"])

            return Device(self.client, id)

    @property
    def permission(self):
        if self.client.asyncio:
            return self.loader.load("permission")
        else:
            return self.client.query('{fileValue(id:"%s"){permission}}' % self._id, keys=[
                "fileValue", "permission"])

    @permission.setter
    def permission(self, newValue):
        self.client.mutation(
            'mutation{fileValue(id:"%s", permission:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def value(self):
        if self.client.asyncio:
            return self.loader.load("value")
        else:
            return self.client.query('{fileValue(id:"%s"){value}}' % self._id, keys=[
                "fileValue", "value"])

    @property
    def fileName(self):
        if self.client.asyncio:
            return self.loader.load("fileName")
        else:
            return self.client.query('{fileValue(id:"%s"){fileName}}' % self._id, keys=[
                "fileValue", "fileName"])

    @property
    def mimeType(self):
        if self.client.asyncio:
            return self.loader.load("mimeType")
        else:
            return self.client.query('{fileValue(id:"%s"){mimeType}}' % self._id, keys=[
                "fileValue", "mimeType"])
