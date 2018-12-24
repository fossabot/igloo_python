import requests
import asyncio
import pathlib
import ssl
import websockets
import json

url = "https://igloo-production.herokuapp.com/graphql"


class Client:
    def __init__(self, token="", username="", password="", newUser=False):
        if token != "":
            self.token = token
        elif username != "" and password != "":
            if newUser:
                self.token = self.signUp(username, password)
            else:
                self.token = self.logIn(username, password)
        else:
            raise Exception("No token or username-password provided")

    def query(self, query, authenticated=True):
        payload = {"query": query}
        headers = {
            'content-type': "application/json",
        }

        if authenticated:
            headers["authorization"] = "Bearer " + self.token

        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers)

        parsedRes = json.loads(response.text)
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

    def logIn(self, username, password):
        query = """
mutation{
  logIn(email:"%s",password:"%s") {
    token
  }
}
""" % (username, password)

        response = self.query(query, authenticated=False)

        return response["logIn"]["token"]

    def signUp(self, username, password):
        query = """
mutation{
  signUp(email:"%s",password:"%s") {
    token
  }
}
""" % (username, password)

        response = self.query(query, authenticated=False)

        return response["SignupUser"]["token"]
