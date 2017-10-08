from twilioSettings import client

holdMessage = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/holdmessage.xml'

class Call(object):
    def __init__(self, toNumber, contact):
        self.toNumber = toNumber
        self.fromNumber = "+15042296824 ",
        self.url = holdMessage
        self.sid = None
        self.callStatus = 'not-started'
        self.contact = contact

    def startCall(self, route):
        call = client.calls.create(
            to = self.toNumber,
            from_ = self.fromNumber,
            url = route,
            method = "GET"
        )
        self.callStatus = call.status
        self.sid = call.sid
        return self

    def updateCallStatus(self):
        call = client.calls(self.sid).fetch()
        self.callStatus = call.status
        return self

    def rerouteCall(self, route):
        call = client.calls(self.sid).update(url = route, method="GET")
        return self

    def endCall(self):
        call = client.calls(self.sid).update(status="completed")
        return self
