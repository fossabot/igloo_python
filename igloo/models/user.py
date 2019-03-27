from .environment import Environment


class User:
    def __init__(self, client):
        self.client = client

    @property
    def name(self):
        res = self.client.query('{user{name}}', keys=["user", "name"])
        return res

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{user(name:"%s"){id}}' % (newName), asyncio=False)

    @property
    def profileIconColor(self):
        res = self.client.query('{user{profileIconColor}}',
                                keys=["user", "profileIconColor"])
        return res

    @property
    def pendingEnvironmentShareCount(self):
        res = self.client.query('{user{pendingEnvironmentShareCount}}', keys=[
                                "user", "pendingEnvironmentShareCount"])
        return res

    @property
    def pendingOwnerChangeCount(self):
        res = self.client.query('{user{pendingOwnerChangeCount}}', keys=[
                                "user", "pendingOwnerChangeCount"])
        return res

    @property
    def environmentCount(self):
        res = self.client.query('{user{environmentCount}}', keys=[
                                "user", "environmentCount"])
        return res

    @property
    def deviceCount(self):
        res = self.client.query('{user{deviceCount}}', keys=[
                                "user", "deviceCount"])
        return res

    @property
    def valueCount(self):
        res = self.client.query('{user{valueCount}}', keys=[
                                "user", "valueCount"])
        return res

    @property
    def notificationCount(self):
        res = self.client.query('{user{notificationCount}}', keys=[
                                "user", "notificationCount"])
        return res

    @property
    def permanentTokenCount(self):
        res = self.client.query('{user{permanentTokenCount}}', keys=[
                                "user", "permanentTokenCount"])
        return res

    @property
    def quietMode(self):
        res = self.client.query('{user{quietMode}}', keys=[
                                "user", "quietMode"])
        return res

    @quietMode.setter
    def quietMode(self, newMode):
        self.client.mutation(
            'mutation{user(quietMode:%s){id}}' % (newMode), asyncio=False)

    @property
    def devMode(self):
        res = self.client.query('{user{devMode}}', keys=["user", "devMode"])
        return res

    @devMode.setter
    def devMode(self, newMode):
        self.client.mutation(
            'mutation{user(devMode:%s){id}}' % (newMode), asyncio=False)

    @property
    def emailIsVerified(self):
        res = self.client.query('{user{emailIsVerified}}', keys=[
                                "user", "emailIsVerified"])
        return res

    @property
    def environments(self):
        return EnvironmentList(self.client)


class EnvironmentList:
    def __init__(self, client):
        self.client = client
        self.current = 0

    def __len__(self):
        res = self.client.query('{user{environmentCount}}', keys=[
                                "user", "environmentCount"])
        return res

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
