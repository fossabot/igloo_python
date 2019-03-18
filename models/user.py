from models.environment import Environment


class User:
    def __init__(self, client):
        self.client = client

    @property
    def name(self):
        res = self.client.query('{user{name}}')
        return res["user"]["name"]

    @name.setter
    def name(self, newName):
        self.client.mutation('mutation{user(name:"%s"){id}}' % (newName))

    @property
    def environments(self):
        return EnvironmentList(self.client)


class EnvironmentList:
    def __init__(self, client):
        self.client = client
        self.current = 0

    def __len__(self):
        res = self.client.query('{user{environmentCount}}')
        return res["user"]["environmentCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user{environments(limit:1, offset:%d){id}}}' % i)
            if len(res["user"]["environments"]) != 1:
                raise IndexError()
            return Environment(self.client, res["user"]["environments"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user{environments(offset:%d, limit:%d){id}}}' % (start, end-start))
            return [Environment(self.client, environment["id"]) for environment in res["user"]["environments"]]
        else:
            print("i", type(i))
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user{environments(limit:1, offset:%d){id}}}' % self.current)

        if len(res["user"]["environments"]) != 1:
            raise StopIteration

        self.current += 1
        return Environment(self.client, res["user"]["environments"][0]["id"])

    def next(self):
        return self.__next__()
