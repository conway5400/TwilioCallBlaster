from twilio.rest import Client
import time

holdMessage = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/holdmessage.xml'

account_sid = "AC4a7cb7028d915e895cdcfd031e89f5da"
auth_token = "9033452bc7ab446c9624e7331f585939"
client = Client(account_sid, auth_token)

class Contact(object):
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber
        self.call = []

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

class CallBank(object):
    def __init__(self, callBankId):
        self.id = callBankId
        self.calls = []
        self.initialRoute = holdMessage
        self.secondaryRoute = None
        self.rerouted = False

    def addCall(self, call):
        self.calls.append(call)
        return self

    def removeCall(self, phoneNumber):
        for index, call in enumerate(self.calls):
            if call.toNumber == phoneNumber:
                self.calls.pop(index)
        return self

    def rerouteAllCalls(self):
        for call in self.calls:
            call.rerouteCall(self.secondaryRoute)
        return self

    def startAllCalls(self, route):
        self.secondaryRoute = route
        for call in self.calls:
            call.startCall()
        return self

    def endAllCalls(self):
        for call in self.calls:
            call.endCall()
        return self

    def getCall(self, phoneNumber):
        for call in self.calls:
            if call.toNumber == phoneNumber:
                return call

    def getCallBankStatus(self):
        print "CHECKING CALL BANK...There are {} calls in this bank!".format(len(self.calls))
        allCallsInProgress = True 
        for call in self.calls:
            print call.callStatus
            call.updateCallStatus()
            if call.callStatus != 'in-progress' and call.callStatus != 'busy' and call.callStatus != 'completed':
                allCallsInProgress = False

        if(allCallsInProgress is True and self.rerouted is False):
            print "ALL CALLS ARE IN PROGRESS ... RE-ROUTING CALLS"
            self.rerouted = True
            self.rerouteAllCalls()

        return allCallsInProgress

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

class ConferenceRooms(object):
    def __init__(self):
        self.conferences = []
        self.name = 'ConferenceRoom1'

    def getActiveConferences(self):
        tempConferences = []

        conferenceList = client.conferences.list(status="in-progress")
        for conference in conferenceList:
            tempConferences.append(conference)

        self.conferences = tempConferences
        return self

    def endAllConferences(self):
        for conference in self.conferences:
            url = "https://api.twilio.com/2010-04-01/Accounts/" + account_sid + "/Conferences/" + conference.sid + ".json"
            result = requests.request('POST', url, data = {u'Status': u'completed'}, auth=('AC4a7cb7028d915e895cdcfd031e89f5da', '9033452bc7ab446c9624e7331f585939'))
            print result
        return self
