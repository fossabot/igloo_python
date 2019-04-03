from .device import Device
from aiodataloader import DataLoader


class EnvironmentLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self.id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{environment(id:"%s"){%s}}' % (self.id, fields), keys=["environment"])

        resolvedValues = [res[key] for key in keys]

        return resolvedValues


class Environment:
    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.loader = EnvironmentLoader(client, id)

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{environment(id:"%s"){name}}' % self.id, keys=[
                "environment", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{environment(id:"%s", name:"%s"){id}}' % (self.id, newName), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{environment(id:"%s"){myRole}}' % self.id, keys=[
                "environment", "myRole"])

    @property
    def picture(self):
        if self.client.asyncio:
            return self.loader.load("picture")
        else:
            return self.client.query('{environment(id:"%s"){picture}}' % self.id, keys=[
                "environment", "picture"])

    @picture.setter
    def picture(self, newPicture):
        self.client.mutation(
            'mutation{environment(id:"%s", picture:"%s"){id}}' % (self.id, newPicture), asyncio=False)

    @property
    def uniqueFirmwares(self):
        if self.client.asyncio:
            return self.loader.load("uniqueFirmwares")
        else:
            return self.client.query('{environment(id:"%s"){uniqueFirmwares}}' % self.id, keys=[
                "environment", "uniqueFirmwares"])

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{environment(id:"%s"){index}}' % self.id, keys=[
                "environment", "index"])

    @index.setter
    def index(self, newIndex):
        self.client.mutation(
            'mutation{environment(id:"%s", index:%s){id}}' % (self.id, newIndex), asyncio=False)

    @property
    def muted(self):
        if self.client.asyncio:
            return self.loader.load("muted")
        else:
            return self.client.query('{environment(id:"%s"){muted}}' % self.id, keys=[
                "environment", "muted"])

    @muted.setter
    def muted(self, newMuted):
        self.client.mutation(
            'mutation{environment(id:"%s", muted:%s){id}}' % (self.id, "true" if newMuted else "false"), asyncio=False)

    @property
    def devices(self):
        return DeviceList(self.client, self.id)


class DeviceList:
    def __init__(self, client, environmentId):
        self.client = client
        self.environmentId = environmentId
        self.current = 0

    def __len__(self):
        res = self.client.query(
            '{environment(id:"%s"){deviceCount}}' % self.environmentId)
        return res["environment"]["deviceCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{environment(id:"%s"){devices(limit:1, offset:%d){id}}}' % (self.environmentId, i))
            if len(res["environment"]["devices"]) != 1:
                raise IndexError()
            return Device(self.client, res["environment"]["devices"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{environment(id:"%s"){devices(offset:%d, limit:%d){id}}}' % (self.environmentId, start, end-start))
            return [Device(self.client, device["id"]) for device in res["environment"]["devices"]]
        else:
            print("i", type(i))
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{environment(id:"%s"){devices(limit:1, offset:%d){id}}}' % (self.environmentId, self.current))

        if len(res["environment", "devices"]) != 1:
            raise StopIteration

        self.current += 1
        return Device(self.client, res["environment"]["devices"][0]["id"])

    def next(self):
        return self.__next__()
