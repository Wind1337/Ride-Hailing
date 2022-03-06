class DriverNode:
    driverID = 0

    def __init__(self, name, carType, seatCapacity, location):
        DriverNode.driverID += 1
        self.driverID = DriverNode.driverID
        self.name = name
        self.carType = carType
        self.seatCapacity = seatCapacity
        self.location = location
        self.next = None
        self.prev = None


class DriverLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def getHead(self):
        return self.head

    def insertAtHead(self, node):
        if self.head is None:
            self.head = self.tail = node
        else:
            self.head.prev = node
            node.next = self.head
            self.head = node

    def insertAtTail(self, node):
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def search(self, inputID):
        temp = self.head
        while temp is not None:
            if temp.driverID == inputID:
                return temp
            temp = temp.next
        print("Not Found")

    def delete(self, inputID):
        temp = self.head
        while temp is not None:
            if temp.driverID != inputID:
                temp = temp.next
            else:
                if temp == self.head:
                    self.head = self.head.next
                    #self.head.prev = None
                elif temp == self.tail:
                    self.tail = self.tail.prev
                    #self.tail.next = None
                else:
                    prev = temp.prev
                    succ = temp.next
                    prev.next = succ
                    succ.prev = prev
                del temp
                return
        print("Not Found")
