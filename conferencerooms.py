from flask import request
from twilioSettings import client

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
