from .environment import Environment


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
    def profileIconColor(self):
        res = self.client.query('{user{profileIconColor}}')
        return res["user"]["profileIconColor"]

    @property
    def pendingEnvironmentShareCount(self):
        res = self.client.query('{user{pendingEnvironmentShareCount}}')
        return res["user"]["pendingEnvironmentShareCount"]

    @property
    def pendingOwnerChangeCount(self):
        res = self.client.query('{user{pendingOwnerChangeCount}}')
        return res["user"]["pendingOwnerChangeCount"]

    @property
    def environmentCount(self):
        res = self.client.query('{user{environmentCount}}')
        return res["user"]["environmentCount"]

    @property
    def deviceCount(self):
        res = self.client.query('{user{deviceCount}}')
        return res["user"]["deviceCount"]

    @property
    def valueCount(self):
        res = self.client.query('{user{valueCount}}')
        return res["user"]["valueCount"]

    @property
    def notificationCount(self):
        res = self.client.query('{user{notificationCount}}')
        return res["user"]["notificationCount"]

    @property
    def permanentTokenCount(self):
        res = self.client.query('{user{permanentTokenCount}}')
        return res["user"]["permanentTokenCount"]

    @property
    def quietMode(self):
        res = self.client.query('{user{quietMode}}')
        return res["user"]["quietMode"]

    @quietMode.setter
    def quietMode(self, newMode):
        self.client.mutation('mutation{user(quietMode:%s){id}}' % (newMode))

    @property
    def devMode(self):
        res = self.client.query('{user{devMode}}')
        return res["user"]["devMode"]

    @devMode.setter
    def devMode(self, newMode):
        self.client.mutation('mutation{user(devMode:%s){id}}' % (newMode))

    @property
    def emailIsVerified(self):
        res = self.client.query('{user{emailIsVerified}}')
        return res["user"]["emailIsVerified"]

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
