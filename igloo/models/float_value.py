class FloatValue:
    def __init__(self, client, id):
        self.client = client
        self.id = id

    @property
    def name(self):
        res = self.client.query('{floatValue(id:"%s"){name}}' %
                                self.id, keys=["floatValue", "name"])
        return res

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{floatValue(id:"%s", name:"%s"){id}}' % (self.id, newName), asyncio=False)
