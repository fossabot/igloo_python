class PlotValue:
    def __init__(self, client, id):
        self.client = client
        self.id = id

    @property
    def name(self):
        res = self.client.query('{plotValue(id:"%s"){name}}' %
                                self.id, keys=["plotValue", "name"])
        return res

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{plotValue(id:"%s", name:"%s"){id}}' % (self.id, newName), asyncio=False)
