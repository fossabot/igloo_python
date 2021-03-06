
from aiodataloader import DataLoader
from .utils import wrapWith


class PermanentTokenLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{permanentToken(id:"%s"){%s}}' % (self._id, fields), keys=["permanentToken"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching device{id} the result is in the device key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class PermanentToken:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = PermanentTokenLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        if self.client.asyncio:
            res = self.loader.load("user{id}")
        else:
            res = self.client.query('{permanentToken(id:"%s"){user{id}}}' % self._id, keys=[
                "permanentToken", "user"])

        from .user import User

        def wrapper(res):
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{permanentToken(id:"%s"){name}}' % self._id, keys=[
                "permanentToken", "name"])


class PermanentTokenList:
    def __init__(self, client):
        self.client = client
        self.current = 0

    def __len__(self):
        res = self.client.query(
            '{user{permanentTokenCount}}')
        return res["user"]["permanentTokenCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user{permanentTokens(limit:1, offset:%d){id}}}' % (i))
            if len(res["user"]["permanentTokens"]) != 1:
                raise IndexError()
            return PermanentToken(self.client, res["user"]["permanentTokens"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user{permanentTokens(offset:%d, limit:%d){id}}}' % (start, end-start))
            return [PermanentToken(self.client, token["id"]) for token in res["user"]["permanentTokens"]]
        else:
            print("i", type(i))
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user{permanentTokens(limit:1, offset:%d){id}}}' % (self.current))

        if len(res["user", "permanentTokens"]) != 1:
            raise StopIteration

        self.current += 1
        return PermanentToken(self.client, res["user"]["permanentTokens"][0]["id"])

    def next(self):
        return self.__next__()
