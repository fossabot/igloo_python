
from aiodataloader import DataLoader


class NotificationLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{notification(id:"%s"){%s}}' % (self._id, fields), keys=["device"])

        resolvedValues = [res[key] for key in keys]

        return resolvedValues


class Notification:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = NotificationLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def content(self):
        if self.client.asyncio:
            return self.loader.load("content")
        else:
            return self.client.query('{notification(id:"%s"){content}}' %
                                     self._id, keys=["notification", "content"])

    @content.setter
    def content(self, newContent):
        self.client.mutation(
            'mutation{notification(id:"%s", content:"%s"){id}}' % (self._id, newContent), asyncio=False)

    @property
    def date(self):
        if self.client.asyncio:
            return self.loader.load("date")
        else:
            return self.client.query('{notification(id:"%s"){date}}' %
                                     self._id, keys=["notification", "date"])

    @property
    def read(self):
        if self.client.asyncio:
            return self.loader.load("read")
        else:
            return self.client.query('{notification(id:"%s"){read}}' %
                                     self._id, keys=["notification", "read"])
