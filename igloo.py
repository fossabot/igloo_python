import requests
import asyncio
import pathlib
import ssl
import websockets
import json
from models.user import User
from models.environment import Environment
from models.device import Device
url = "https://iglooql.herokuapp.com/graphql"


class GraphQLException(Exception):
    pass


class Client:
    def __init__(self, token):
        self.token = token

    def query(self, query, variables=None, authenticated=True):
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

        return parsedRes["data"]

    mutation = query

    async def subscribe(self, query):
        async with websockets.connect(
                'wss://igloo-production.herokuapp.com/subscriptions', ssl=True, subprotocols=["graphql-ws"]) as websocket:
            await websocket.send('{"type":"connection_init","payload":{"Authorization":"Bearer %s"}}' % (self.token))

            res = await websocket.recv()
            if json.loads(res)["type"] != "connection_ack":
                raise Exception("failed to connect")

            await websocket.send('{"id":"1","type":"start","payload":{"query":"%s","variables":null}}' % (query))
            while True:
                response = await websocket.recv()
                parsedResponse = json.loads(response)

                if parsedResponse["type"] == "data":
                    yield parsedResponse["payload"]["data"]
