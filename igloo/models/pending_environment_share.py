
from aiodataloader import DataLoader


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
