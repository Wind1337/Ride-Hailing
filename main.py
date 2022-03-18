from flask import *
from Passenger import *
from Driver import *
from Matching import *

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
        selectedPass = request.form.get("selectedPass")
        print(selectedPass)

        return redirect(url_for('index'))
    else:
        singlePassArray = []
        sharedPassArray = []
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

        for i in range(len(matchResultList)):
            singlePassArray.append(matchResultList[i].get('passengerName'))

        for i in range(len(sharedMatchResultList)):
            sharedPassArray.append(sharedMatchResultList[i].get('passenger1Name'))
            sharedPassArray.append(sharedMatchResultList[i].get('passenger2Name'))

        return render_template('index.html', route=route, singlePassArray=singlePassArray,
                               sharedPassArray=sharedPassArray)


if __name__ == '__main__':
    app.run(debug=True)
