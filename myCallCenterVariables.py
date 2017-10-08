from myPackages import CallBanks, CallBank, Contact, Call
from SeedNumbers import seedNumbers

#routes for music and selections
musicRoom = 'https://storage.googleapis.com/spectrum-interactive-test-bucket/musicMessage.xml'
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
