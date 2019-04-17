from aiodataloader import DataLoader


class UserLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{user(id:"%s"){%s}}' % (self._id, fields), keys=["user"])

        resolvedValues = [res[key] for key in keys]

        return resolvedValues


class User:
    def __init__(self, client, id=None):
        self.client = client

        if id is None:
            self._id = self.client.query(
                '{user{id}}', keys=["user", "id"], asyncio=False)
        else:
            self._id = id

        self.loader = UserLoader(client, self._id)

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        if self.client.asyncio:
            return self.loader.load("email")
        else:
            return self.client.query('{user(id:"%s"){email}}' % self._id, keys=["user", "email"])

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{user(id:"%s"){name}}' % self._id, keys=["user", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{user(id:"%s")(name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def profileIconColor(self):
        if self.client.asyncio:
            return self.loader.load("profileIconColor")
        else:
            return self.client.query('{user(id:"%s"){profileIconColor}}' % self._id,
                                     keys=["user", "profileIconColor"])

    @property
    def quietMode(self):
        if self.client.asyncio:
            return self.loader.load("quietMode")
        else:
            return self.client.query('{user(id:"%s"){quietMode}}' % self._id, keys=[
                "user", "quietMode"])

    @quietMode.setter
    def quietMode(self, newMode):
        self.client.mutation(
            'mutation{user(id:"%s")(quietMode:%s){id}}' % (self._id, "true" if newMode else "false"), asyncio=False)

    @property
    def devMode(self):
        if self.client.asyncio:
            return self.loader.load("devMode")
        else:
            return self.client.query('{user(id:"%s"){devMode}}' % self._id, keys=["user", "devMode"])

    @devMode.setter
    def devMode(self, newMode):
        self.client.mutation(
            'mutation{user(id:"%s")(devMode:%s){id}}' % (self._id, "true" if newMode else "false"), asyncio=False)

    @property
    def emailIsVerified(self):
        if self.client.asyncio:
            return self.loader.load("emailIsVerified")
        else:
            return self.client.query('{user(id:"%s"){emailIsVerified}}' % self._id, keys=[
                "user", "emailIsVerified"])

    @property
    def primaryAuthenticationMethods(self):
        if self.client.asyncio:
            return self.loader.load("primaryAuthenticationMethods")
        else:
            return self.client.query('{user(id:"%s"){primaryAuthenticationMethods}}' % self._id, keys=[
                "user", "primaryAuthenticationMethods"])

    @property
    def secondaryAuthenticationMethods(self):
        if self.client.asyncio:
            return self.loader.load("secondaryAuthenticationMethods")
        else:
            return self.client.query('{user(id:"%s"){secondaryAuthenticationMethods}}' % self._id, keys=[
                "user", "secondaryAuthenticationMethods"])

    @property
    def environments(self):
        from .environment import EnvironmentList
        return EnvironmentList(self.client)

    @property
    def pendingEnvironmentShares(self):
        from .pending_environment_share import UserPendingEnvironmentShareList
        return UserPendingEnvironmentShareList(self.client)

    @property
    def pendingOwnerChanges(self):
        from .pending_owner_change import UserPendingOwnerChangeList
        return UserPendingOwnerChangeList(self.client)

    @property
    def developerDevices(self):
        from .device import DeveloperDeviceList
        return DeveloperDeviceList(self.client)

    @property
    def permanentTokens(self):
        from .permanent_token import PermanentTokenList
        return PermanentTokenList(self.client)
