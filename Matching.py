import Driver
import Passenger


def match(DriverList, PassengerList):
    matchList = []
    currentPassenger = PassengerList.getHead()
    while currentPassenger is not None:
        currentDriver = DriverList.getHead()
        while currentDriver is not None:
            if currentPassenger.pickup == currentDriver.location and currentPassenger.reqSeatCapacity <= currentDriver.seatCapacity and currentPassenger.reqCarType == currentDriver.carType:
                matchList.append([currentPassenger, currentDriver])
                DriverList.delete(currentDriver.driverID)
                PassengerList.delete(currentPassenger.passengerID)
                break
            else:
                currentDriver = currentDriver.next
        currentPassenger = currentPassenger.next
    return matchList


testDriverLinkedList = Driver.DriverLinkedList()
testPassengerLinkedList = Passenger.PassengerLinkedList()

testDriver = Driver.DriverNode("Tan Ah Kow", "Standard", 4, 367532495)
print(testDriver.driverID)
testPassenger = Passenger.PassengerNode("Xiao Ming", 367532495, 7103759997, "Standard", 4)
print(testPassenger.passengerID)
testDriverLinkedList.insertAtTail(testDriver)
testPassengerLinkedList.insertAtTail(testPassenger)

testDriver = Driver.DriverNode("Tan Ah Ming", "Standard", 6, 243702776)
print(testDriver.driverID)
testPassenger = Passenger.PassengerNode("Big Ming", 243702776, 5202652823, "Standard", 4)
print(testPassenger.passengerID)
testDriverLinkedList.insertAtTail(testDriver)
testPassengerLinkedList.insertAtTail(testPassenger)

result = match(testDriverLinkedList, testPassengerLinkedList)
print("Matched", result[0][0].name, "and", result[0][1].name)
print("Matched", result[1][0].name, "and", result[1][1].name)
