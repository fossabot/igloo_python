class Device:
    def __init__(self, client, id):
        self.client = client
        self.id = id

    @property
    def name(self):
        res = self.client.query('{device(id:"%s"){name}}' %
                                self.id, keys=["device", "name"])
        return res

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{device(id:"%s", name:"%s"){id}}' % (self.id, newName), blocking=True)
