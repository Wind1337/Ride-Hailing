from flask import *
from Passenger import *
from Driver import *
from Matching import *
from geopy.geocoders import Nominatim

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
    scenario = 2
    detail = [[0 for column in range(4)] for row in range(scenario)]

    for index in range(len(matchResultList)):
        detail[index][0] = (matchResultList[index].get('passengerName'))
        detail[index][1] = (matchResultList[index].get('driverName'))
        detail[index][2] = Nominatim(user_agent="Geocoder").reverse(
            str(matchResultList[index].get('passengerPickupLat')) + "," + str(
                matchResultList[index].get('passengerPickupLong'))).address
        detail[index][3] = Nominatim(user_agent="Geocoder").reverse(
            str(matchResultList[index].get('passengerDropoffLat')) + "," + str(
                matchResultList[index].get('passengerDropoffLong'))).address

    if request.method == 'POST':
        passenger_name = request.form.get("selectedPass")
        index, plot = route(passenger_name)

        return render_template('index.html', index=index, plot=plot, detail=detail)
    else:
        plot = [[0 for column in range(2)] for row in range(1)]

        plot[0][0] = matchResultList[0].get("passengerPickupLat")
        plot[0][1] = matchResultList[0].get("passengerPickupLong")


        return render_template('index.html', index=0, plot=plot, detail=detail)


def route(passenger_name):
    locate = 0

    for index in range(len(matchResultList)):

        if matchResultList[index].get('passengerName') == passenger_name:
            # pick_up = matchResultList[index].get("passengerPickup")
            locate = index
            node_list = []

            with open("output/route.json") as file:
                data = json.load(file)

                for element in data['path']:
                    node_list.append(element)

            plot = [[0 for column in range(2)] for row in range(len(node_list))]

            with open("data/nodes.json") as file:
                data = json.load(file)

                for index in range(len(node_list)):

                    for element in data['nodes']:

                        if element['nodeID'] == node_list[index]:
                            plot[index][0] = element['latitude']
                            plot[index][1] = element['longitude']

    return locate, plot


if __name__ == '__main__':
    app.run(debug=True)
