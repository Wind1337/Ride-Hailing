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


def approxDistance(fromNodeID, toNodeID, nodeDict):
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
    nodeDict = importNodes(nodeRaw)
    matchList = []
    sharedMatchList = []
    currentPassenger = PassengerList.getHead()
    while currentPassenger is not None:
        reqSeatCapacity = currentPassenger.reqSeatCapacity
        passengerPickup = currentPassenger.pickup
        reqCarType = currentPassenger.reqCarType
        currentDriver = DriverList.getHead()
        if currentPassenger.reqSharedRide == True:
            sharedMatch(currentPassenger, PassengerList, DriverList, sharedMatchList, nodeDict)
        else:
            while currentDriver is not None:
                driverLocation = currentDriver.location
                driverSeatCapacity = currentDriver.seatCapacity
                driverCarType = currentDriver.carType
                distance = approxDistance(passengerPickup, driverLocation, nodeDict)
                if distance < 1000 and reqSeatCapacity <= driverSeatCapacity and reqCarType == driverCarType:
                    matchList.append([currentPassenger, currentDriver])
                    DriverList.delete(currentDriver.driverID)
                    PassengerList.delete(currentPassenger.passengerID)
                    break
                else:
                    currentDriver = currentDriver.next
        currentPassenger = currentPassenger.next
    return matchList, sharedMatchList


def sharedMatch(currentPassenger, PassengerList, DriverList, sharedMatchList, nodeDict):
    currentPassenger1 = currentPassenger
    currentDriver = DriverList.getHead()
    currentPassenger = currentPassenger.next
    while currentPassenger is not None:
        if currentPassenger.reqSharedRide != True:
            currentPassenger = currentPassenger.next
        else:
            currentPassenger2 = currentPassenger
            pickupDistanceDelta = approxDistance(currentPassenger1.pickup, currentPassenger2.pickup, nodeDict)
            dropoffDistanceDelta = approxDistance(currentPassenger1.dropoff, currentPassenger2.dropoff, nodeDict)
            if pickupDistanceDelta > 1000 and dropoffDistanceDelta > 1000:
                currentPassenger = currentPassenger.next
            else:
                passengerPickup1 = currentPassenger1.pickup
                passengerPickup2 = currentPassenger2.pickup
                while currentDriver is not None:
                    driverLocation = currentDriver.location
                    distance1 = approxDistance(passengerPickup1, driverLocation, nodeDict)
                    distance2 = approxDistance(passengerPickup2, driverLocation, nodeDict)
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
