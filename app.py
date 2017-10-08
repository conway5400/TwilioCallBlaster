from myPackages import *
from myCallCenterVariables import *
app = Flask(__name__)


@app.route('/')
def landingPageRoute():
    return render_template('index.html', allCallBanks = allCallBanks)

@app.route('/callChange', methods=['POST'])
def callChangeRoute():
    # get variables from POST request
    action = request.form['action']
    origin = request.form['origin']
    routing = request.form['routing']
    route = getRoute(routing)
    phoneNumber = request.form['phoneNumber']

    # get variables
    originCallBank = allCallBanks.getCallBank(origin)
    originCall = originCallBank.getCall(phoneNumber)
    targetCallBank = allCallBanks.getCallBank(routing)

    #check action and handle solution
    if action == 'end':
        originCall.endCall()
    else:
        if targetCallBank is None:
            newCallBank = CallBank(routing)
            allCallBanks.callBanks.append(newCallBank)
            newCallBank.addCall(originCall)
        else:
            targetCallBank.addCall(originCall)

        if action == 'start':
            originCall.startCall(route)
        elif action == 'reroute':
            originCall.rerouteCall(route)

        originCallBank.removeCall(originCall)
    return "complete"

@app.route('/startAllCalls',methods=['POST'])
def startAllCallsRoute():
    route = getRoute(request.form['routing'])
    inactiveCallBank.startAllCalls(route)

    return "started all inactive calls"

@app.route('/endAllCalls',methods=['POST'])
def endAllCallsRoute():
    allCallBanks.endAllCalls();
    ConferenceRooms().getActiveConferences().endAllConferences()
    return "ended all calls and conferences"

@app.route('/callsStatus')
def getCallsStatus():
    status = allCallBanks.getAllCallBanksStatus()
    allCallBanksJson = jsonpickle.encode(status)
    return allCallBanksJson

def getRoute(routing):
    route = ''
    #determine routing
    if routing == 'musicRoom':
        route = musicRoom
    elif routing == 'confRoom1':
        route = confRoom1
    elif routing == 'confRoom2':
        route = confRoom2
    elif routing == 'confRoom3':
        route = confRoom3

    return route

app.run(debug=True)

