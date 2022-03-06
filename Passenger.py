class PassengerNode:
    passengerID = 0

    def __init__(self, name, pickup, dropoff, reqCarType, reqSeatCapacity):
        PassengerNode.passengerID += 1
        self.passengerID = PassengerNode.passengerID
        self.name = name
        self.pickup = pickup
        self.dropoff = dropoff
        self.reqCarType = reqCarType
        self.reqSeatCapacity = reqSeatCapacity
        self.next = None
        self.prev = None


class PassengerLinkedList:
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
            if temp.passengerID == inputID:
                return temp
            temp = temp.next
        print("Not Found")

    def delete(self, inputID):
        temp = self.head
        while temp is not None:
            if temp.passengerID != inputID:
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
