class CallBanks(object):
    def __init__(self):
        self.callBanks = []

    def addCallBank(self, callBank):
        self.callBanks.append(callBank)
        return self

    def getCallBank(self, callBankId):
        for callBank in self.callBanks:
            if callBank.id == callBankId:
                return callBank

    def endAllCalls(self):
        for callBank in self.callBanks:
            for call in callBank.calls:
                call.endCall()
