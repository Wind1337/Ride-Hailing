import Driver
import Passenger
import json
import math

nodeJson = open('data/nodes.json')
nodeRaw = json.load(nodeJson)


def importNodes(nodeRaw):
    nodeDict = {}
    for i in nodeRaw["nodes"]:
        cords = []
        cords.append(i["latitude"])
        cords.append(i["longitude"])
        nodeDict[i["nodeID"]] = cords
    # print(nodeDict.get(236676523))
    return nodeDict


def approxDistance(fromNodeID, toNodeID):
    global nodeDict
    fromCord = nodeDict.get(fromNodeID)
    toCord = nodeDict.get(toNodeID)
    latDis = math.radians(toCord[0] - fromCord[0])
    longDis = math.radians(toCord[1] - fromCord[1])
    a = pow(math.sin(latDis / 2), 2) + math.cos(math.radians(fromCord[0])) * math.cos(math.radians(toCord[0])) * \
        pow(math.sin(longDis / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dis = (6371 * 1000) * c  # Distance in metres
    return dis


def match(DriverList, PassengerList):
    matchList = []
    sharedMatchList = []
    currentPassenger = PassengerList.getHead()
    while currentPassenger is not None:
        reqSeatCapacity = currentPassenger.reqSeatCapacity
        passengerPickup = currentPassenger.pickup
        reqCarType = currentPassenger.reqCarType
        currentDriver = DriverList.getHead()
        if currentPassenger.reqSharedRide == True:
            sharedMatch(currentPassenger, PassengerList, DriverList, sharedMatchList)
        else:
            while currentDriver is not None:
                driverLocation = currentDriver.location
                driverSeatCapacity = currentDriver.seatCapacity
                driverCarType = currentDriver.carType
                distance = approxDistance(passengerPickup, driverLocation)
                if distance < 1000 and reqSeatCapacity <= driverSeatCapacity and reqCarType == driverCarType:
                    matchList.append([currentPassenger, currentDriver])
                    DriverList.delete(currentDriver.driverID)
                    PassengerList.delete(currentPassenger.passengerID)
                    break
                else:
                    currentDriver = currentDriver.next
        currentPassenger = currentPassenger.next
    return matchList, sharedMatchList


def sharedMatch(currentPassenger, PassengerList, DriverList, sharedMatchList):
    currentPassenger1 = currentPassenger
    currentDriver = DriverList.getHead()
    currentPassenger = currentPassenger.next
    while currentPassenger is not None:
        if currentPassenger.reqSharedRide != True:
            currentPassenger = currentPassenger.next
        else:
            currentPassenger2 = currentPassenger
            pickupDistanceDelta = approxDistance(currentPassenger1.pickup, currentPassenger2.pickup)
            dropoffDistanceDelta = approxDistance(currentPassenger1.dropoff, currentPassenger2.dropoff)
            if pickupDistanceDelta > 1000 and dropoffDistanceDelta > 1000:
                currentPassenger = currentPassenger.next
            else:
                passengerPickup1 = currentPassenger1.pickup
                passengerPickup2 = currentPassenger2.pickup
                while currentDriver is not None:
                    driverLocation = currentDriver.location
                    distance1 = approxDistance(passengerPickup1, driverLocation)
                    distance2 = approxDistance(passengerPickup2, driverLocation)
                    if (distance1 < 1000):
                        sharedMatchList.append([currentPassenger1, currentPassenger2, currentDriver])
                        DriverList.delete(currentDriver.driverID)
                        PassengerList.delete(currentPassenger1.passengerID)
                        PassengerList.delete(currentPassenger2.passengerID)
                        return
                    elif (distance2 < 1000):
                        sharedMatchList.append([currentPassenger2, currentPassenger1, currentDriver])
                        DriverList.delete(currentDriver.driverID)
                        PassengerList.delete(currentPassenger1.passengerID)
                        PassengerList.delete(currentPassenger2.passengerID)
                        return
                    else:
                        currentDriver = currentDriver.next
                currentPassenger = currentPassenger.next


nodeDict = importNodes(nodeRaw)

testDriverLinkedList = Driver.DriverLinkedList()
testPassengerLinkedList = Passenger.PassengerLinkedList()

testDriver = Driver.DriverNode("Tan Ah Kow", "Standard", 4, 614066679)
testPassenger = Passenger.PassengerNode("Xiao Ming", 367532495, 7103759997, "Standard", 4, False)
testDriverLinkedList.insertAtTail(testDriver)
testPassengerLinkedList.insertAtTail(testPassenger)

testDriver = Driver.DriverNode("Tan Ah Ming", "Standard", 6, 243702776)
testPassenger = Passenger.PassengerNode("Big Ming", 243702776, 5202652823, "Standard", 4, False)
testDriverLinkedList.insertAtTail(testDriver)
testPassengerLinkedList.insertAtTail(testPassenger)

testPassenger = Passenger.PassengerNode("Shared 1", 243702776, 5202652823, "Standard", 2, True)
testPassengerLinkedList.insertAtTail(testPassenger)
testPassenger = Passenger.PassengerNode("Shared 2", 243702776, 5202652823, "Standard", 2, True)
testPassengerLinkedList.insertAtTail(testPassenger)
testDriver = Driver.DriverNode("Shared Driver 1", "Standard", 6, 243702776)
testDriverLinkedList.insertAtTail(testDriver)

matchResult, sharedMatchResult = match(testDriverLinkedList, testPassengerLinkedList)
matchResultList = []
matchResultDict = {"matchResult": matchResultList}
for i in range(len(matchResult)):
    matchAttrDict = {}
    # Passenger Attributes
    matchAttrDict["passengerName"] = matchResult[i][0].fullname
    matchAttrDict["passengerPickup"] = matchResult[i][0].pickup
    matchAttrDict["passengerPickupLat"] = nodeDict.get(matchResult[i][0].pickup)[0]
    matchAttrDict["passengerPickupLong"] = nodeDict.get(matchResult[i][0].pickup)[1]
    matchAttrDict["passengerDropoff"] = matchResult[i][0].dropoff
    matchAttrDict["passengerDropoffLat"] = nodeDict.get(matchResult[i][0].dropoff)[0]
    matchAttrDict["passengerDropoffLong"] = nodeDict.get(matchResult[i][0].dropoff)[1]
    matchAttrDict["passengerCarType"] = matchResult[i][0].reqCarType
    matchAttrDict["passengerSeatCapacity"] = matchResult[i][0].reqSeatCapacity
    # Driver Attributes
    matchAttrDict["driverName"] = matchResult[i][1].fullname
    matchAttrDict["driverLocation"] = matchResult[i][1].location
    matchAttrDict["driverLocationLat"] = nodeDict.get(matchResult[i][1].location)[0]
    matchAttrDict["driverLocationLong"] = nodeDict.get(matchResult[i][1].location)[1]
    matchAttrDict["driverCarType"] = matchResult[i][1].carType
    matchAttrDict["driverSeatCapacity"] = matchResult[i][1].seatCapacity
    matchResultList.append(matchAttrDict)
    '''print("Matched:", matchResult[i][0].fullname, "and", matchResult[i][1].fullname)'''

sharedMatchResultList = []
sharedMatchResultDict = {"sharedMatchResult": sharedMatchResultList}
for i in range(len(sharedMatchResult)):
    sharedMatchAttrDict = {}
    # 1st Passenger to Pickup
    sharedMatchAttrDict["passenger1Name"] = sharedMatchResult[i][0].fullname
    sharedMatchAttrDict["passenger1Pickup"] = sharedMatchResult[i][0].pickup
    sharedMatchAttrDict["passenger1PickupLat"] = nodeDict.get(sharedMatchResult[i][0].pickup)[0]
    sharedMatchAttrDict["passenger1PickupLong"] = nodeDict.get(sharedMatchResult[i][0].pickup)[1]
    sharedMatchAttrDict["passenger1Dropoff"] = sharedMatchResult[i][0].dropoff
    sharedMatchAttrDict["passenger1DropoffLat"] = nodeDict.get(sharedMatchResult[i][0].dropoff)[0]
    sharedMatchAttrDict["passenger1DropoffLong"] = nodeDict.get(sharedMatchResult[i][0].dropoff)[1]
    # 2nd Passenger to Pickup
    sharedMatchAttrDict["passenger2Name"] = sharedMatchResult[i][1].fullname
    sharedMatchAttrDict["passenger2Pickup"] = sharedMatchResult[i][1].pickup
    sharedMatchAttrDict["passenger2PickupLat"] = nodeDict.get(sharedMatchResult[i][1].pickup)[0]
    sharedMatchAttrDict["passenger2PickupLong"] = nodeDict.get(sharedMatchResult[i][1].pickup)[1]
    sharedMatchAttrDict["passenger2Dropoff"] = sharedMatchResult[i][1].dropoff
    sharedMatchAttrDict["passenger2DropoffLat"] = nodeDict.get(sharedMatchResult[i][1].dropoff)[0]
    sharedMatchAttrDict["passenger2DropoffLong"] = nodeDict.get(sharedMatchResult[i][1].dropoff)[1]
    # Driver Attributes
    sharedMatchAttrDict["driverName"] = sharedMatchResult[i][2].fullname
    sharedMatchAttrDict["driverLocation"] = sharedMatchResult[i][2].location
    sharedMatchAttrDict["driverLocationLat"] = nodeDict.get(sharedMatchResult[i][2].location)[0]
    sharedMatchAttrDict["driverLocationLong"] = nodeDict.get(sharedMatchResult[i][2].location)[1]
    sharedMatchAttrDict["driverCarType"] = sharedMatchResult[i][2].carType
    sharedMatchAttrDict["driverSeatCapacity"] = sharedMatchResult[i][2].seatCapacity
    sharedMatchResultList.append(sharedMatchAttrDict)
    '''print("Shared Matched Passengers:", sharedMatchResult[i][0].fullname, "and", sharedMatchResult[i][1].fullname,
          "and driver:", sharedMatchResult[i][2].fullname)'''

json_object = json.dumps(matchResultDict, indent=4)
with open("./output/match.json", "w") as outfile:
    outfile.write(json_object)

json_object = json.dumps(sharedMatchResultDict, indent=4)

with open("./output/sharedMatch.json", "w") as outfile:
    outfile.write(json_object)
