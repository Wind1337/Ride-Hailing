from flask import *

import Matching
import Driver
import Passenger
import geopy.geocoders
from geopy.geocoders import Nominatim
from routing import route, routewithtraffic

import certifi
import ssl

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

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

    if request.method == "POST":
        find_route(request.form.get("selectedPass"), request.form.get("trafficChecked"))

        return render_template('index.html', data=dictionary)
    else:
        plot = [[nodeDict.get(matchResult[0][0].pickup)[1], nodeDict.get(matchResult[0][0].pickup)[0]]]
        dictionary["detail"].append([" ", " ", " ", " "])

        dictionary["index"] = len(dictionary["detail"]) - 1
        dictionary["route"] = plot
        dictionary["marker"] = ""
        dictionary["passenger_1"] = None

        return render_template('index.html', data=dictionary)


def find_route(passenger_name, traffic):
    route_path = []
    plot = []
    marker = []
    passenger_index = edges = 0

    try:
        dictionary["passenger_1"], dictionary["passenger_2"] = passenger_name.split(" & ")
    except ValueError:
        dictionary["passenger_1"] = passenger_name

    for index in range(len(matchResult)):

        if dictionary["passenger_1"] == matchResult[index][0].fullname:
            passenger_index = index
            node = [matchResult[index][1].location, matchResult[index][0].pickup, matchResult[index][0].dropoff]

            marker.append([nodeDict.get(matchResult[passenger_index][0].pickup)[1],
                           nodeDict.get(matchResult[passenger_index][0].pickup)[0]])
            marker.append([nodeDict.get(matchResult[passenger_index][0].dropoff)[1],
                           nodeDict.get(matchResult[passenger_index][0].dropoff)[0]])
            break

        try:
            if dictionary["passenger_1"] == sharedMatchResult[index][0].fullname:
                passenger_index = index + len(matchResult)
                node = [sharedMatchResult[index][2].location, sharedMatchResult[index][0].pickup,
                        sharedMatchResult[index][1].pickup, sharedMatchResult[index][0].dropoff,
                        sharedMatchResult[index][1].dropoff]

                marker.append([nodeDict.get(sharedMatchResult[index][0].pickup)[1],
                               nodeDict.get(sharedMatchResult[index][0].pickup)[0]])
                marker.append([nodeDict.get(sharedMatchResult[index][0].dropoff)[1],
                               nodeDict.get(sharedMatchResult[index][0].dropoff)[0]])
                marker.append([nodeDict.get(sharedMatchResult[index][1].pickup)[1],
                               nodeDict.get(sharedMatchResult[index][1].pickup)[0]])
                marker.append([nodeDict.get(sharedMatchResult[index][1].dropoff)[1],
                               nodeDict.get(sharedMatchResult[index][1].dropoff)[0]])
                break
        except IndexError:
            pass

    for counter in range(len(node) - 1):
        dictionary["traffic"] = traffic

        if traffic is None:
            temp = route(node[counter], node[counter + 1])
        else:
            temp = routewithtraffic(node[counter], node[counter + 1])

        for element in temp:
            route_path.append(element)

    for index in range(len(route_path)):
        for element in nodes_data['nodes']:
            if element['nodeID'] == route_path[index]:
                with open("data/edges.json") as edges_file:
                    edges_data = json.load(edges_file)
                    for token in edges_data['edges']:
                        try:
                            if token['fromNode'] == route_path[index] and token['toNode'] == route_path[index + 1]:
                                for data in token['coordinates']:
                                    plot.append(data)
                                edges += 1
                        except:
                            pass
                if edges == 0:
                    plot.append([element['longitude'], element['latitude']])
                    edges = 0

    dictionary["index"] = passenger_index
    dictionary["route"] = plot
    dictionary["marker"] = marker


def importDriverPassenger():
    DriverLinkedList = Driver.DriverLinkedList()
    PassengerLinkedList = Passenger.PassengerLinkedList()

    with open("data/drivers.json") as driver_file:
        driver_data = json.load(driver_file)

    with open("data/passengers.json") as passengers_file:
        passenger_data = json.load(passengers_file)

    for i in driver_data["drivers"]:
        driver = Driver.DriverNode(i["driverName"], i["driverCarType"], i["driverSeatCapacity"], i["driverLocation"])
        DriverLinkedList.insertAtTail(driver)

    for i in passenger_data["passengers"]:
        if i["passengerShared"] == "True":
            shared = True
        else:
            shared = False
        passenger = Passenger.PassengerNode(i["passengerName"], i["passengerPickup"], i["passengerDropoff"],
                                            i["passengerCarType"], i["passengerSeatCapacity"], shared)
        PassengerLinkedList.insertAtTail(passenger)

    return DriverLinkedList, PassengerLinkedList


if __name__ == '__main__':
    DriverLinkedList, PassengerLinkedList = importDriverPassenger()
    matchResult, sharedMatchResult = Matching.match(DriverLinkedList, PassengerLinkedList)
    dictionary = {"just_ride": len(matchResult)}
    detail = []

    with open("data/nodes.json") as nodes_file:
        nodes_data = json.load(nodes_file)

    nodeDict = Matching.importNodes(nodes_data)

    for index in range(len(matchResult)):
        passenger_name = matchResult[index][0].fullname
        driver_name = matchResult[index][1].fullname
        pickup = Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(matchResult[index][0].pickup)[0]) + "," + str(
                nodeDict.get(matchResult[index][0].pickup)[1])).address
        dropoff = Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(matchResult[index][0].dropoff)[0]) + "," + str(
                nodeDict.get(matchResult[index][0].dropoff)[1])).address

        detail.append([passenger_name, driver_name, pickup, dropoff])

    for index in range(len(sharedMatchResult)):
        passenger_name = str(sharedMatchResult[index][0].fullname) + " & " + str(sharedMatchResult[index][1].fullname)
        driver_name = sharedMatchResult[index][2].fullname
        pickup = Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(sharedMatchResult[index][0].pickup)[0]) + "," + str(
                nodeDict.get(sharedMatchResult[index][0].pickup)[1])).address + "AND" + Nominatim(user_agent="Geocoder",
                                                                                                  timeout=3).reverse(
            str(nodeDict.get(sharedMatchResult[index][1].pickup)[0]) + "," + str(
                nodeDict.get(sharedMatchResult[index][1].pickup)[1])).address
        dropoff = Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(sharedMatchResult[index][0].dropoff)[0]) + "," + str(
                nodeDict.get(sharedMatchResult[index][0].dropoff)[1])).address + "AND" + Nominatim(
            user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(sharedMatchResult[index][1].dropoff)[0]) + "," + str(
                nodeDict.get(sharedMatchResult[index][1].dropoff)[1])).address

        detail.append([passenger_name, driver_name, pickup, dropoff])

    dictionary['detail'] = detail
    dictionary["size"] = len(dictionary["detail"])

    app.run(debug=True)
