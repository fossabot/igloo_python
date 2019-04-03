
from aiodataloader import DataLoader


class NotificationLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self.id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{notification(id:"%s"){%s}}' % (self.id, fields), keys=["device"])

        resolvedValues = [res[key] for key in keys]

        return resolvedValues


class Notification:
    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.loader = NotificationLoader(client, id)

    @property
    def content(self):
        if self.client.asyncio:
            return self.loader.load("content")
        else:
            return self.client.query('{notification(id:"%s"){content}}' %
                                     self.id, keys=["notification", "content"])

    @content.setter
    def content(self, newContent):
        self.client.mutation(
            'mutation{notification(id:"%s", content:"%s"){id}}' % (self.id, newContent), asyncio=False)

    @property
    def date(self):
        if self.client.asyncio:
            return self.loader.load("date")
        else:
            return self.client.query('{notification(id:"%s"){date}}' %
                                     self.id, keys=["notification", "date"])

    @property
    def read(self):
        if self.client.asyncio:
            return self.loader.load("read")
        else:
            return self.client.query('{notification(id:"%s"){read}}' %
                                     self.id, keys=["notification", "read"])
