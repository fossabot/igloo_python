from .environment import EnvironmentList
from .pending_environment_share import UserPendingEnvironmentShareList
from .pending_owner_change import UserPendingOwnerChangeList
from .device import DeveloperDeviceList
from .permanent_token import PermanentTokenList
from aiodataloader import DataLoader


class UserLoader(DataLoader):
    def __init__(self, client):
        super().__init__()
        self.client = client

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{user{%s}}' % fields, keys=["user"])

        resolvedValues = [res[key] for key in keys]

        return resolvedValues


class User:
    def __init__(self, client):
        self.client = client
        self.loader = UserLoader(client)

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        if self.client.asyncio:
            return self.loader.load("email")
        else:
            return self.client.query('{user{email}}', keys=["user", "email"])

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{user{name}}', keys=["user", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{user(name:"%s"){id}}' % (newName), asyncio=False)

    @property
    def profileIconColor(self):
        if self.client.asyncio:
            return self.loader.load("profileIconColor")
        else:
            return self.client.query('{user{profileIconColor}}',
                                     keys=["user", "profileIconColor"])

    @property
    def quietMode(self):
        if self.client.asyncio:
            return self.loader.load("quietMode")
        else:
            return self.client.query('{user{quietMode}}', keys=[
                "user", "quietMode"])

    @quietMode.setter
    def quietMode(self, newMode):
        self.client.mutation(
            'mutation{user(quietMode:%s){id}}' % ("true" if newMode else "false"), asyncio=False)

    @property
    def devMode(self):
        if self.client.asyncio:
            return self.loader.load("devMode")
        else:
            return self.client.query('{user{devMode}}', keys=["user", "devMode"])

    @devMode.setter
    def devMode(self, newMode):
        self.client.mutation(
            'mutation{user(devMode:%s){id}}' % ("true" if newMode else "false"), asyncio=False)

    @property
    def emailIsVerified(self):
        if self.client.asyncio:
            return self.loader.load("emailIsVerified")
        else:
            return self.client.query('{user{emailIsVerified}}', keys=[
                "user", "emailIsVerified"])

    @property
    def primaryAuthenticationMethods(self):
        if self.client.asyncio:
            return self.loader.load("primaryAuthenticationMethods")
        else:
            return self.client.query('{user{primaryAuthenticationMethods}}', keys=[
                "user", "primaryAuthenticationMethods"])

    @property
    def secondaryAuthenticationMethods(self):
        if self.client.asyncio:
            return self.loader.load("secondaryAuthenticationMethods")
        else:
            return self.client.query('{user{secondaryAuthenticationMethods}}', keys=[
                "user", "secondaryAuthenticationMethods"])

    @property
    def environments(self):
        return EnvironmentList(self.client)

    @property
    def pendingEnvironmentShares(self):
        return UserPendingEnvironmentShareList(self.client)

    @property
    def pendingOwnerChanges(self):
        return UserPendingOwnerChangeList(self.client)

    @property
    def developerDevices(self):
        return DeveloperDeviceList(self.client)

    @property
    def permanentTokens(self):
        return PermanentTokenList(self.client)
