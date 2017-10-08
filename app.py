from twilioProjectClasses import CallBanks, CallBank, Contact, Call, ConferenceRooms
from flask import Flask, render_template, request, redirect
from twilio.rest import Client
import time
import requests
import json
import jsonpickle
from SeedNumbers import seedNumbers

app = Flask(__name__)

# Get these credentials from http://twilio.com/user/account
account_sid = "AC4a7cb7028d915e895cdcfd031e89f5da"
auth_token = "9033452bc7ab446c9624e7331f585939"
client = Client(account_sid, auth_token)

holdMessage = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/holdmessage.xml'
musicMessage = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/musicMessage.xml'
conferenceRoomMessage = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/conferenceRoomMessage.xml'

#routes
muiscRoom = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/musicMessage.xml'
confRoom1 = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/conferenceRoom1.xml'
confRoom2 = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/conferenceRoom2.xml'
confRoom3 = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/conferenceRoom3.xml'

#create address book and call bank
allCallBanks = CallBanks()
inactiveCallBank = CallBank("inactiveRoom")

allCallBanks.addCallBank(inactiveCallBank);

#seed data for call banks and calls

for seedNumber in seedNumbers:
    contact = Contact(seedNumber['name'], seedNumber['phoneNumber'])
    call = Call(contact.phoneNumber, contact)
    inactiveCallBank.addCall(call)


@app.route('/')
def landingPageRoute():
    return render_template('index.html', allCallBanks = allCallBanks)

@app.route('/startAllCalls',methods=['POST'])
def startCallsRoute():
    callBank.rerouted = False
    if request.form['routing'] == 'musicMessage':
        route = musicMessage
    elif request.form['routing'] == 'conferenceRoomMessage':
        route = conferenceRoomMessage
    else:
        route = musicMessage
    callBank.startAllCalls(route)
    return "started"


@app.route('/startCall', methods=['POST'])
def startCallRoute():
    origin = request.form['origin']
    routing = request.form['routing']
    phoneNumber = request.form['phoneNumber']

    originCallBank = allCallBanks.getCallBank(origin)
    originCall = originCallBank.getCall(phoneNumber)
    targetCallBank = allCallBanks.getCallBank(routing)

    if targetCallBank is None:
        newCallBank = CallBank(routing)
        allCallBanks.callBanks.append(newCallBank)
        newCallBank.addCall(originCall)
    else:
        targetCallBank.addCall(originCall)

    route = ''

    if routing == 'musicRoom':
        route = muiscRoom
    elif routing == 'confRoom1':
        route = confRoom1
    elif routing == 'confRoom2':
        route = confRoom1
    elif routing == 'confRoom3':
        route = confRoom1

    print route

    originCall.startCall(route)
    originCallBank.removeCall(originCall)
        
    return "started"

@app.route('/endCall', methods=['POST'])
def endCallRoute():
    origin = request.form['origin']
    phoneNumber = request.form['phoneNumber']

    originCallBank = allCallBanks.getCallBank(origin)
    originCall = originCallBank.getCall(phoneNumber)
    originCall.endCall()

    originCallBank.removeCall(originCall)
    targetCallBank = allCallBanks.getCallBank('inactiveRoom').addCall(originCall)
    return "ended"

@app.route('/rerouteCall', methods=['POST'])
def rerouteCallRoute():
    origin = request.form['origin']
    routing = request.form['routing']
    phoneNumber = request.form['phoneNumber']

    originCallBank = allCallBanks.getCallBank(origin)
    originCall = originCallBank.getCall(phoneNumber)
    targetCallBank = allCallBanks.getCallBank(routing)

    if targetCallBank is None:
       newCallBank = CallBank(routing)
       allCallBanks.callBanks.append(newCallBank)
       newCallBank.addCall(originCall)
    else:
       targetCallBank.addCall(originCall)

    route = ''

    if routing == 'musicRoom':
        route = muiscRoom
    elif routing == 'confRoom1':
        route = confRoom1
    elif routing == 'confRoom2':
        route = confRoom2
    elif routing == 'confRoom3':
        route = confRoom3

    print route

    originCall.rerouteCall(route)
    originCallBank.removeCall(originCall)
    return "rerouted"


@app.route('/endCalls',methods=['POST'])
def endCallsRoute():
    callBank.endAllCalls()
    ConferenceRooms().getActiveConferences().endAllConferences()
    
    if callBank.secondaryRoute == 'musicMessage':
        callBank.endAllCalls()
    elif callBank.secondaryRoute == 'conferenceRoomMessage':
        ConferenceRooms().getActiveConferences().endAllConferences()
    return "complete"

@app.route('/callsStatus')
def getCallsStatus():
    status = callBank.getCallBankStatus()
    addressBookJson = jsonpickle.encode(addressBook)
    return addressBookJson

app.run(debug=True)
