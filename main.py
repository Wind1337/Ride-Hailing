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

        return render_template('index.html', detail=detail, index=passenger_index, just_ride=just_ride,
                               size=len(detail), route=plot)
    else:
        plot.append([nodeDict.get(matchResult[0][0].pickup)[0], nodeDict.get(matchResult[0][0].pickup)[1]])
        detail.append([" ", " ", " ", " "])

        return render_template('index.html', detail=detail, index=len(detail) - 1, just_ride=just_ride,
                               size=len(detail), route=plot)


def find_route(passenger_name):

    try:
        passenger_1, passenger_2 = passenger_name.split(" & ")
    except ValueError:
        passenger_1 = passenger_name

    plot = []
    passenger_index = edge = 0

    with open("data/edges.json") as file:
        edges = json.load(file)

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


if __name__ == '__main__':
    just_ride = 4
    detail = []

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

    app.run(debug=True)
