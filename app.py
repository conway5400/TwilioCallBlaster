from flask import Flask, render_template, request, redirect
from twilio.rest import Client
import time
import requests

app = Flask(__name__)

# Get these credentials from http://twilio.com/user/account
account_sid = "AC4a7cb7028d915e895cdcfd031e89f5da"
auth_token = "9033452bc7ab446c9624e7331f585939"
client = Client(account_sid, auth_token)

holdMessage = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/holdmessage.xml'
musicMessage = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/musicMessage.xml'
conferenceRoomMessage = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/conferenceRoomMessage.xml'

class AddressBook(object):
    def __init__(self):
        self.contacts = []

    def addContact(self, contact):
        self.contacts.append(contact)

class Contact(object):
    def __init__(self, phoneNumber):
        self.name = "Conway Solomon"
        self.phoneNumber = phoneNumber

class CallBank(object):
    def __init__(self, name):
        self.name = name
        self.calls = []
        self.initialRoute = holdMessage
        self.secondaryRoute = None

    def addCall(self, call):
        self.calls.append(call)
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

    def getCallBankStatus(self):
        print "CHECKING CALL BANK...There are {} calls in this bank!".format(len(self.calls))
        allCallsInProgress = True 
        for call in self.calls:
            print call.callStatus
            if call.callStatus != 'in-progress':
                allCallsInProgress = False
                call.updateCallStatus()
                break

        if(allCallsInProgress is True):
            print "ALL CALLS ARE IN PROGRESS ... RE-ROUTING CALLS"
            self.rerouteAllCalls()
        else:
            print "ALL CALLS ARE NOT YET IN PROGRESS"
            time.sleep(2)
            self.getCallBankStatus()

        return allCallsInProgress

class Call(object):
    def __init__(self, toNumber):
        self.toNumber = toNumber
        self.fromNumber = "+15043387662",
        self.url = holdMessage
        self.twilioCall = None,
        self.sid = None
        self.callStatus = 'not-started'

    def startCall(self):
        call = client.calls.create(
            to = self.toNumber,
            from_ = self.fromNumber,
            url = self.url,
            method = "GET"
        )
        self.callStatus = call.status
        self.twilioCall = call
        self.sid = call.sid
        return self

    def updateCallStatus(self):
        if self.callStatus != 'not-started':
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

#create address book and call bank
addressBook = AddressBook()
callBank = CallBank("Main Call Bank")

#seed data for address book and contacts
seedNumbers = ["+15043387662"]
for seedNumber in seedNumbers:
    addressBook.addContact(Contact(seedNumber)) 

#seed data for call banks and calls
for contact in addressBook.contacts:
    call = Call(contact.phoneNumber)
    callBank.addCall(call)

@app.route('/')
def landingPageRoute():
    print addressBook.contacts[0].__dict__
    return render_template('index.html', contacts = addressBook.contacts)

@app.route('/startCalls',methods=['POST'])
def startCallsRoute():
    if request.form['routing'] == 'musicMessage':
        route = musicMessage
    elif request.form['routing'] == 'conferenceRoomMessage':
        route = conferenceRoomMessage
    else:
        route = musicMessage
    print "ROUTE" + route
    print "ROUTING" + request.form['routing']
    callBank.startAllCalls(route).getCallBankStatus()
    return "complete"

@app.route('/endCalls',methods=['POST'])
def endCallsRoute():
    callBank.endAllCalls()
    ConferenceRooms().getActiveConferences().endAllConferences()
    
    if callBank.secondaryRoute == 'musicMessage':
        callBank.endAllCalls()
    elif callBank.secondaryRoute == 'conferenceRoomMessage':
        ConferenceRooms().getActiveConferences().endAllConferences()
    return "complete"

app.run(debug=True)
