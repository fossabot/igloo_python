class MutationRoot:
    def __init__(self, client):
        self.client = client

    def verifyPassword(self, email, password):
        return self.client.mutation(
            """mutation{ verifyPassword(email:"%s",password:"%s")}""" % (email, password))["verifyPassword"]

    def verifyWebAuthn(self, challengeResponse, jwtChallenge):
        return self.client.mutation(
            """mutation{ verifyWebAuthn(challengeResponse:"%s",jwtChallenge:"%s")}""" % (challengeResponse, jwtChallenge))["verifyWebAuthn"]
