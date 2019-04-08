import requests
import asyncio
import pathlib
import ssl
import websockets
import json
from .models.user import User
from .models.environment import Environment
from .models.device import Device
from .models.float_value import FloatValue
from .mutations import MutationRoot
from .subscriptions import SubscriptionRoot
from .utils import get_from_dict
from aiohttp import ClientSession
import asyncio

host = "bering.igloo.ooo"
url = "https://{}/graphql".format(host)


class GraphQLException(Exception):
    pass


class Client:
    def __init__(self, token, asyncio=False):
        self.token = token
        self.session = ClientSession()
        self.asyncio = asyncio

    def set_token(self, newToken):
        self.token = newToken

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__close__())

    async def __close__(self):
        await self.session.close()

    @property
    def query_root(self):
        return QueryRoot(self)

    @property
    def mutation_root(self):
        return MutationRoot(self)

    @property
    def subscription_root(self):
        return SubscriptionRoot(self)

    async def __async_query(self, query, variables=None, keys=[]):
        payload = {"query": query}
        if variables != None:
            payload["variables"] = variables

        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + self.token
        }

        async with self.session.post(url, data=json.dumps(payload), headers=headers) as response:
            parsedRes = await response.json()

        if "errors" in parsedRes.keys():
            raise GraphQLException(parsedRes["errors"][0]["message"])

        return get_from_dict(parsedRes, ["data", *keys])

    def __sync_query(self, query, variables=None, keys=[]):
        payload = {"query": query}
        if variables != None:
            payload["variables"] = variables

        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + self.token
        }

        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)

        parsedRes = json.loads(response.text)
        if "errors" in parsedRes.keys():
            raise GraphQLException(parsedRes["errors"][0]["message"])

        return get_from_dict(parsedRes, ["data", *keys])

    def query(self, query, variables=None, keys=[], asyncio=None):
        if asyncio == False or (asyncio is None and not self.asyncio):
            return self.__sync_query(query, variables=variables, keys=keys)
        else:
            return self.__async_query(query, variables=variables, keys=keys)

    mutation = query

    async def subscribe(self, query):
        async with websockets.connect(
                'wss://{}/subscriptions'.format(host), ssl=True, subprotocols=["graphql-ws"]) as websocket:
            await websocket.send('{"type":"connection_init","payload":{"Authorization":"Bearer %s"}}' % (self.token))

            res = await websocket.recv()
            if json.loads(res)["type"] != "connection_ack":
                raise Exception("failed to connect")

            listen_query_message = '{"id":"1","type":"start","payload":{"query":"%s","variables":null}}' % (
                query.replace('"', '\\"')
            )
            await websocket.send(listen_query_message)
            while True:
                response = await websocket.recv()
                parsedResponse = json.loads(response)
                if parsedResponse["type"] == "data":
                    print(parsedResponse)
                    yield parsedResponse["payload"]["data"]


class QueryRoot:
    def __init__(self, client):
        self.client = client

    @property
    def user(self):
        return User(self.client)

    def environment(self, id):
        return Environment(self.client, id)

    def device(self, id):
        return Device(self.client, id)
