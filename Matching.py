import json
import math

nodeJson = open('data/nodes.json')
nodeRaw = json.load(nodeJson)


# Read nodes from JSON file and construct a dictionary
# Key: Node ID
# Value: [Lat, Long]
def importNodes(nodeRaw):
    nodeDict = {}
    for i in nodeRaw["nodes"]:
        cords = []
        cords.append(i["latitude"])
        cords.append(i["longitude"])
        nodeDict[i["nodeID"]] = cords
    return nodeDict


# Calculate straight line distance between 2 nodes
# This uses the Haversine formula
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


# Matching algorithm
def match(DriverList, PassengerList):
    # Import Node Dictionary
    nodeDict = importNodes(nodeRaw)
    # Initialize match lists
    matchList = []
    sharedMatchList = []
    # Start at Passenger Linked List head
    currentPassenger = PassengerList.getHead()
    # Iterate through all the passengers
    while currentPassenger is not None:
        # Read requested seat capacity, pickup and requested car type from passenger node
        reqSeatCapacity = currentPassenger.reqSeatCapacity
        passengerPickup = currentPassenger.pickup
        reqCarType = currentPassenger.reqCarType
        # Get driver linked list head
        currentDriver = DriverList.getHead()
        # If the passenger wants a shared ride, call the shared ride match algorithm
        if currentPassenger.reqSharedRide == True:
            sharedMatch(currentPassenger, PassengerList, DriverList, sharedMatchList, nodeDict)
        else:
            # Iterate through all the drivers to find a match
            while currentDriver is not None:
                # Get driver location, seat capacity and car type
                driverLocation = currentDriver.location
                driverSeatCapacity = currentDriver.seatCapacity
                driverCarType = currentDriver.carType
                # Get the straight line distance between the driver and passenger
                distance = approxDistance(passengerPickup, driverLocation, nodeDict)
                # Match condition: Straight line distance under 1km
                # Match condition: Driver seat capacity > Passenger requested capacity
                # Match condition: Passenger requested car type = Driver car type
                if distance < 1000 and reqSeatCapacity <= driverSeatCapacity and reqCarType == driverCarType:
                    # Match found, add the driver and passenger to the match result array
                    matchList.append([currentPassenger, currentDriver])
                    # Delete the matched driver and passenger from the Linked List
                    DriverList.delete(currentDriver.driverID)
                    PassengerList.delete(currentPassenger.passengerID)
                    break
                else:
                    # If driver is not suitable, go to the next driver in the list
                    currentDriver = currentDriver.next
        # Go to the next passenger
        currentPassenger = currentPassenger.next
    # Return the result lists
    return matchList, sharedMatchList


# Shared ride matching algorithm
def sharedMatch(currentPassenger, PassengerList, DriverList, sharedMatchList, nodeDict):
    # Get the passenger and the head of the driver linked list
    currentPassenger1 = currentPassenger
    currentDriver = DriverList.getHead()
    # Get the next in line in passenger linked list
    currentPassenger = currentPassenger.next
    # Iterate through all the passengers
    while currentPassenger is not None:
        # If passenger does not want a shared ride, go next
        if currentPassenger.reqSharedRide != True:
            currentPassenger = currentPassenger.next
        else:
            # Get the 2nd potential passenger
            currentPassenger2 = currentPassenger
            # Get the straight line distance between the 2 passenger's pick up points
            pickupDistanceDelta = approxDistance(currentPassenger1.pickup, currentPassenger2.pickup, nodeDict)
            # Get the straight line distance between the 2 passenger's drop-off points
            dropoffDistanceDelta = approxDistance(currentPassenger1.dropoff, currentPassenger2.dropoff, nodeDict)
            # Go next if the distance between the 2 points are more than 1km apart
            if pickupDistanceDelta > 1000 or dropoffDistanceDelta > 1000:
                currentPassenger = currentPassenger.next
            else:
                # Find a suitable driver
                passengerPickup1 = currentPassenger1.pickup
                passengerPickup2 = currentPassenger2.pickup
                # Iterate through the driver linked list
                while currentDriver is not None:
                    # Get driver location
                    driverLocation = currentDriver.location
                    # Measure distance between the driver location and the 2 passenger pickup locations
                    distance1 = approxDistance(passengerPickup1, driverLocation, nodeDict)
                    distance2 = approxDistance(passengerPickup2, driverLocation, nodeDict)
                    # If Passenger 1 is under 1km from the driver, pick him up first
                    if (distance1 < 1000):
                        sharedMatchList.append([currentPassenger1, currentPassenger2, currentDriver])
                        DriverList.delete(currentDriver.driverID)
                        PassengerList.delete(currentPassenger1.passengerID)
                        PassengerList.delete(currentPassenger2.passengerID)
                        return
                    # Else if Passenger 2 is under 1km from the driver, pick him up first
                    elif (distance2 < 1000):
                        sharedMatchList.append([currentPassenger2, currentPassenger1, currentDriver])
                        DriverList.delete(currentDriver.driverID)
                        PassengerList.delete(currentPassenger1.passengerID)
                        PassengerList.delete(currentPassenger2.passengerID)
                        return
                    # If both distance conditions do not match, go to the next driver
                    else:
                        currentDriver = currentDriver.next
                # Go to the next passenger
                currentPassenger = currentPassenger.next
