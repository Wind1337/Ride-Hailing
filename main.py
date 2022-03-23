from flask import *
from Matching import *
from geopy.geocoders import Nominatim
from routing import route

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
    plot = []

    if request.method == "POST":
        passenger_name = request.form.get("selectedPass")
        passenger_index, plot = find_route(passenger_name)

        return render_template('index.html', detail=detail, index=passenger_index, size=len(detail), route=plot)
    else:
        plot.append([nodeDict.get(matchResult[0][0].pickup)[0], nodeDict.get(matchResult[0][0].pickup)[1]])
        detail.append([" ", " ", " ", " "])

        return render_template('index.html', detail=detail, index=len(detail) - 1, size=len(detail), route=plot)


def find_route(passenger_name):

    try:
        passenger_1, passenger_2 = passenger_name.split(" & ")
    except ValueError:
        passenger_1 = passenger_name

    plot = []
    passenger_index = 0

    for index in range(len(matchResult)):

        if passenger_1 == matchResult[index][0].fullname:
            passenger_index = index
            pickup_node = matchResult[index][0].pickup
            dropoff_node = matchResult[i][0].dropoff

            route_path = route(pickup_node, dropoff_node)

            with open("data/nodes.json") as file:
                data = json.load(file)

                for index in range(len(route_path)):

                    for element in data['nodes']:

                        if element['nodeID'] == route_path[index]:
                            plot.append([element['latitude'], element['longitude']])
                            file.close()

    return passenger_index, plot

    # scenario = 4
    # counter = 0
    # detail = [[0 for column in range(4)] for row in range(scenario)]
    #
    # for index in range(len(matchResultList)):
    #     detail[index][0] = (matchResultList[index].get('passengerName'))
    #     detail[index][1] = (matchResultList[index].get('driverName'))
    #     detail[index][2] = Nominatim(user_agent="Geocoder").reverse(
    #         str(matchResultList[index].get('passengerPickupLat')) + "," + str(
    #             matchResultList[index].get('passengerPickupLong'))).address
    #     detail[index][3] = Nominatim(user_agent="Geocoder").reverse(
    #         str(matchResultList[index].get('passengerDropoffLat')) + "," + str(
    #             matchResultList[index].get('passengerDropoffLong'))).address
    #     counter = index
    #
    # for index in range(len(sharedMatchResult)):
    #     detail[index + (counter + 1)][0] = str(sharedMatchResultList[index].get('passenger1Name')) + " & " + str(
    #         sharedMatchResultList[index].get('passenger2Name'))
    #     detail[index + (counter + 1)][1] = sharedMatchResultList[index].get('driverName')
    #     detail[index + (counter + 1)][2] = Nominatim(user_agent="Geocoder").reverse(
    #         str(sharedMatchResultList[index].get('passenger1PickupLat')) + "," + str(
    #             sharedMatchResultList[index].get('passenger1PickupLong'))).address + "\n" + Nominatim(
    #         user_agent="Geocoder").reverse(str(sharedMatchResultList[index].get('passenger2PickupLat')) + "," + str(
    #         sharedMatchResultList[index].get('passenger2PickupLong'))).address
    #     detail[index + (counter + 1)][3] = Nominatim(user_agent="Geocoder").reverse(
    #         str(sharedMatchResultList[index].get('passenger1DropoffLat')) + "," + str(
    #             sharedMatchResultList[index].get('passenger1DropoffLong'))).address + " AND " + Nominatim(
    #         user_agent="Geocoder").reverse(str(sharedMatchResultList[index].get('passenger2DropoffLat')) + "," + str(
    #         sharedMatchResultList[index].get('passenger2DropoffLong'))).address
    #
    # if request.method == 'POST':
    #     passenger_name = request.form.get("selectedPass")
    #     index, trip, plot = route(scenario - 1, counter, passenger_name)
    #
    #     return render_template('index.html', index=index, detail=detail, just_ride=counter + 1,
    #                            total_scenario=scenario - 1, trip=trip, plot=plot)
    # else:
    #     plot = [[0 for column in range(2)] for row in range(1)]
    #
    #     plot[0][0] = matchResultList[0].get("passengerPickupLat")
    #     plot[0][1] = matchResultList[0].get("passengerPickupLong")
    #     detail[scenario - 1][0] = ""
    #     detail[scenario - 1][1] = ""
    #     detail[scenario - 1][2] = ""
    #     detail[scenario - 1][3] = ""
    #
    #     return render_template('index.html', index=scenario - 1, detail=detail, just_ride=counter + 1,
    #                            total_scenario=scenario - 1, plot=plot)


# def route(scenario, counter, passenger_name):
#     try:
#         passenger_1, passenger_2 = passenger_name.split(" & ")
#     except ValueError:
#         passenger_1 = passenger_name
#
#     locate = 0
#
#     for index in range(scenario):
#
#         if matchResultList[index].get('passengerName') == passenger_1:
#             # pick_up = matchResultList[index].get("passengerPickup")
#             locate = index
#             node_list = []
#             trip = [[0 for column in range(2)] for row in range(3)]
#
#             with open("output/route.json") as file:
#                 data = json.load(file)
#
#                 for element in data['path']:
#                     node_list.append(element)
#
#             plot = [[0 for column in range(2)] for row in range(len(node_list))]
#
#             with open("data/nodes.json") as file:
#                 data = json.load(file)
#
#                 for index in range(len(node_list)):
#
#                     for element in data['nodes']:
#
#                         if element['nodeID'] == node_list[index]:
#                             plot[index][0] = element['latitude']
#                             plot[index][1] = element['longitude']
#             break
#         elif sharedMatchResultList[0].get('passenger1Name') == passenger_1:
#             locate = index + counter + 1
#             node_list = []
#
#             with open("output/route.json") as file:
#                 data = json.load(file)
#
#                 for element in data['path']:
#                     node_list.append(element)
#
#             plot = [[0 for column in range(2)] for row in range(len(node_list))]
#
#             with open("data/nodes.json") as file:
#                 data = json.load(file)
#
#                 for index in range(len(node_list)):
#
#                     for element in data['nodes']:
#
#                         if element['nodeID'] == node_list[index]:
#                             plot[index][0] = element['latitude']
#                             plot[index][1] = element['longitude']
#             break
#
#     return locate, trip, plot

if __name__ == '__main__':

    detail = []
    for index in range(len(matchResult)):
        passenger_name = matchResult[index][0].fullname
        driver_name = matchResult[index][1].fullname
        pickup = Nominatim(user_agent="Geocoder").reverse(
            str(nodeDict.get(matchResult[i][0].pickup)[0]) + "," + str(
                nodeDict.get(matchResult[i][0].pickup)[1])).address
        dropoff = Nominatim(user_agent="Geocoder").reverse(
            str(nodeDict.get(matchResult[i][0].dropoff)[0]) + "," + str(
                nodeDict.get(matchResult[i][0].dropoff)[1])).address

        detail.append([passenger_name, driver_name, pickup, dropoff])

    app.run(debug=True)
