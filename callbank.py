holdMessage = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/holdmessage.xml'

class CallBank(object):
    def __init__(self, callBankId):
        self.id = callBankId
        self.calls = []
        self.allCallsInProgress = False

    def addCall(self, call):
        self.calls.append(call)
        return self

    def removeCall(self, phoneNumber):
        for index, call in enumerate(self.calls):
            if call.toNumber == phoneNumber:
                self.calls.pop(index)
        return self

    def rerouteAllCalls(self, route):
        for call in self.calls:
            call.rerouteCall(route)
        return self

    def startAllCalls(self, route):
        for call in self.calls:
            call.startCall(route)
        return self

    def endAllCalls(self):
        for call in self.calls:
            call.endCall()
        return self

    def getCall(self, phoneNumber):
        for call in self.calls:
            if call.toNumber == phoneNumber:
                return call

    def updateCallBankStatus(self):
        self.allCallsInProgress = True
        for call in self.calls:
            call.updateCallStatus()
            if call.callStatus != 'in-progress' and call.callStatus != 'busy' and call.callStatus != 'completed':
                self.allCallsInProgress = False

        return self
