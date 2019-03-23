from .device import Device


class Environment:
    def __init__(self, client, id):
        self.client = client
        self.id = id

    @property
    def name(self):
        res = self.client.query('{environment(id:"%s"){name}}' % self.id)
        return res["environment"]["name"]

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{environment(id:"%s", name:"%s"){id}}' % (self.id, newName))

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

        if len(res["environment"]["devices"]) != 1:
            raise StopIteration

        self.current += 1
        return Device(self.client, res["environment"]["devices"][0]["id"])

    def next(self):
        return self.__next__()
