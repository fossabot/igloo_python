from aiodataloader import DataLoader
from .utils import wrapWith


class PendingEnvironmentShareLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{pendingEnvironmentShare(id:"%s"){%s}}' % (self._id, fields), keys=["pendingEnvironmentShare"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching device{id} the result is in the device key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class PendingEnvironmentShare:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = PendingEnvironmentShareLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def role(self):
        if self.client.asyncio:
            return self.loader.load("role")
        else:
            return self.client.query('{pendingEnvironmentShare(id:"%s"){role}}' % self._id, keys=[
                "pendingEnvironmentShare", "role"])

    @property
    def sender(self):
        if self.client.asyncio:
            res = self.loader.load("sender{id}")
        else:
            res = self.client.query('{pendingEnvironmentShare(id:"%s"){sender{id}}}' % self._id, keys=[
                "pendingEnvironmentShare", "sender"])

        def wrapper(res):
            from .user import User
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def receiver(self):
        if self.client.asyncio:
            res = self.loader.load("receiver{id}")
        else:
            res = self.client.query('{pendingEnvironmentShare(id:"%s"){receiver{id}}}' % self._id, keys=[
                "pendingEnvironmentShare", "receiver"])

        def wrapper(res):
            from .user import User
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def environment(self):
        if self.client.asyncio:
            res = self.loader.load("environment{id}")
        else:
            res = self.client.query('{pendingEnvironmentShare(id:"%s"){environment{id}}}' % self._id, keys=[
                "pendingEnvironmentShare", "environment"])

        def wrapper(res):
            from .environment import Environment
            return Environment(self.client, res["id"])

        return wrapWith(res, wrapper)


class UserPendingEnvironmentShareList:
    def __init__(self, client):
        self.client = client
        self.current = 0

    def __len__(self):
        res = self.client.query('{user{pendingEnvironmentShareCount}}', keys=[
                                "user", "pendingEnvironmentShareCount"])
        return res

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user{pendingEnvironmentShares(limit:1, offset:%d){id}}}' % i)
            if len(res["user"]["pendingEnvironmentShares"]) != 1:
                raise IndexError()
            return PendingEnvironmentShare(self.client, res["user"]["pendingEnvironmentShares"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user{pendingEnvironmentShares(offset:%d, limit:%d){id}}}' % (start, end-start))
            return [PendingEnvironmentShare(self.client, pendingShare["id"]) for pendingShare in res["user"]["pendingEnvironmentShares"]]
        else:
            print("i", type(i))
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user{pendingEnvironmentShares(limit:1, offset:%d){id}}}' % self.current)

        if len(res["user"]["pendingEnvironmentShares"]) != 1:
            raise StopIteration

        self.current += 1
        return PendingEnvironmentShare(self.client, res["user"]["pendingEnvironmentShares"][0]["id"])

    def next(self):
        return self.__next__()


class EnvironmentPendingEnvironmentShareList:
    def __init__(self, client, environmentId):
        self.client = client
        self.current = 0
        self.environmentId = environmentId

    def __len__(self):
        res = self.client.query('{environment(id:"%s"){pendingEnvironmentShareCount}}' % self.environmentId, keys=[
                                "environment", "pendingEnvironmentShareCount"])
        return res

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{environment(id:"%s"){pendingEnvironmentShares(limit:1, offset:%d){id}}}' % (self.environmentId, i))
            if len(res["environment"]["pendingEnvironmentShares"]) != 1:
                raise IndexError()
            return PendingEnvironmentShare(self.client, res["environment"]["pendingEnvironmentShares"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{environment(id:"%s"){pendingEnvironmentShares(offset:%d, limit:%d){id}}}' % (self.environmentId, start, end-start))
            return [PendingEnvironmentShare(self.client, pendingShare["id"]) for pendingShare in res["environment"]["pendingEnvironmentShares"]]
        else:
            print("i", type(i))
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{environment(id:"%s"){pendingEnvironmentShares(limit:1, offset:%d){id}}}' % (self.environmentId, self.current))

        if len(res["environment"]["pendingEnvironmentShares"]) != 1:
            raise StopIteration

        self.current += 1
        return PendingEnvironmentShare(self.client, res["environment"]["pendingEnvironmentShares"][0]["id"])

    def next(self):
        return self.__next__()
