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
        passenger_index, plot, marker = find_route(passenger_name)

        return render_template('index.html', detail=detail, index=passenger_index, just_ride=just_ride,
                               size=len(detail), route=plot, marker=marker)
    else:
        plot.append([nodeDict.get(matchResult[0][0].pickup)[1], nodeDict.get(matchResult[0][0].pickup)[0]])
        detail.append([" ", " ", " ", " "])

        return render_template('index.html', detail=detail, index=len(detail) - 1, just_ride=just_ride,
                               size=len(detail), route=plot, marker='')


def find_route(passenger_name):
    plot = []
    marker = []
    driver_node = dropoff_node = ""
    passenger_index = edges = 0

    try:
        passenger_1, passenger_2 = passenger_name.split(" & ")
    except ValueError:
        passenger_1 = passenger_name


    for index in range(len(matchResult)):

        if passenger_1 == matchResult[index][0].fullname:
            passenger_index = index
            driver_node = matchResult[index][1].location
            dropoff_node = matchResult[index][0].dropoff

            marker.append([nodeDict.get(matchResult[passenger_index][0].pickup)[1],
                           nodeDict.get(matchResult[passenger_index][0].pickup)[0]])
            marker.append([nodeDict.get(matchResult[passenger_index][0].dropoff)[1],
                           nodeDict.get(matchResult[passenger_index][0].dropoff)[0]])

            break

        try:
            if passenger_1 == sharedMatchResult[index][0].fullname:
                passenger_index = index + just_ride
                driver_node = sharedMatchResult[index][2].location
                dropoff_node = sharedMatchResult[index][0].dropoff

                marker.append([nodeDict.get(sharedMatchResult[index][0].pickup)[1],
                               nodeDict.get(sharedMatchResult[index][0].pickup)[0]])
                marker.append([nodeDict.get(sharedMatchResult[index][0].dropoff)[1],
                               nodeDict.get(sharedMatchResult[index][0].dropoff)[0]])
                marker.append([nodeDict.get(sharedMatchResult[index][1].pickup)[0],
                               nodeDict.get(sharedMatchResult[index][1].pickup)[1]])
                marker.append([nodeDict.get(sharedMatchResult[index][1].dropoff)[1],
                               nodeDict.get(sharedMatchResult[index][1].dropoff)[0]])
                break
        except IndexError:
            pass

    route_path = route(driver_node, dropoff_node)

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

    print(marker)
    return passenger_index, plot, marker


if __name__ == '__main__':
    just_ride = 4
    detail = []

    with open("data/nodes.json") as nodes_file:
        nodes_data = json.load(nodes_file)

    for index in range(len(matchResult)):
        passenger_name = matchResult[index][0].fullname
        driver_name = matchResult[index][1].fullname
        pickup = Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(matchResult[i][0].pickup)[0]) + "," + str(
                nodeDict.get(matchResult[i][0].pickup)[1])).address
        dropoff = Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(matchResult[i][0].dropoff)[0]) + "," + str(
                nodeDict.get(matchResult[i][0].dropoff)[1])).address

        detail.append([passenger_name, driver_name, pickup, dropoff])

    for index in range(len(sharedMatchResult)):
        passenger_name = str(sharedMatchResult[index][0].fullname) + " & " + str(sharedMatchResult[index][1].fullname)
        driver_name = sharedMatchResult[i][2].fullname
        pickup = Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(sharedMatchResult[index][0].pickup)[0]) + "," + str(
                nodeDict.get(sharedMatchResult[index][0].pickup)[1])).address + "AND" + Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(sharedMatchResult[index][1].pickup)[0]) + "," + str(
                nodeDict.get(sharedMatchResult[index][1].pickup)[1])).address
        dropoff = Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(sharedMatchResult[index][0].dropoff)[0]) + "," + str(
                nodeDict.get(sharedMatchResult[index][0].dropoff)[1])).address + "AND" + Nominatim(user_agent="Geocoder", timeout=3).reverse(
            str(nodeDict.get(sharedMatchResult[index][1].dropoff)[0]) + "," + str(
                nodeDict.get(sharedMatchResult[index][1].dropoff)[1])).address

        detail.append([passenger_name, driver_name, pickup, dropoff])

    app.run(debug=True)
