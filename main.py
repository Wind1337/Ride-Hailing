from flask import *
from Passenger import *
from Driver import *
import json

app = Flask(__name__)

# add a SECRET_KEY in the application configuration to take advantage of csrf protection
# and provide a WRF CSRF SECRET_KEY otherwise secret key will be used instead
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        passFullName = request.form.get('passFullName')
        # if passenger form is fill in
        if passFullName is not None:
            passPickUp = request.form.get('passPickUp')
            passDropOff = request.form.get('passDropOff')
            passCarType = request.form.get('passCarType')
            passSeatCapacity = request.form.get('passSeatCapacity')
            passSharedRide = request.form.get('passSharedRide')
            new_passenger(passFullName, passPickUp, passDropOff, passCarType, passSeatCapacity, passSharedRide)
            print("ADDED NEW PASSENGER")
        # if driver form is fill in
        else:
            driFullName = request.form.get('driFullName')
            driCarType = request.form.get('driCarType')
            driSeatCapacity = request.form.get('driSeatCapacity')
            driSharedRide = request.form.get('driSharedRide')
            driLocation = request.form.get('driLocation')
            new_driver(driFullName, driCarType, driSeatCapacity, driSharedRide, driLocation)
            print("ADDED NEW DRIVER")

        return redirect(url_for('index'))
    else:
        '''with open('output/match.json') as file:
            data = json.load(file)

        for element in data['matchResult']:

            print(element["passengerName"], element["passengerPickup"], element["passengerDropoff"], element["driverName"], element["driverLocation"])
        '''

        node = []

        with open("output/route.json") as file:
            data = json.load(file)

            for element in data['path']:
                node.append(element)

        route = [[0 for row in range(2)] for column in range(len(node))]

        with open("data/nodes.json") as file:
            data = json.load(file)

            for index in range(len(node)):

                for element in data['nodes']:

                    if element['nodeID'] == node[index]:
                        route[index][0] = element['latitude']
                        route[index][1] = element['longitude']

        return render_template('index.html', route=route)


if __name__ == '__main__':
    app.run(debug=True)
