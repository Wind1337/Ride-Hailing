class QueueNode:
    def __init__(self, nodeID, cost):
        self.nodeID = nodeID
        self.cost = cost
        self.next = None
        self.prev = None


class QueueLinkedList:
    def __init__(self):
        self.head = None #lowest cost
        self.tail = None #higest cost

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

    def search(self, value):
        temp = self.head
        while temp is not None:
            if temp.data == value:
                return temp
            temp = temp.next
        print("Not Found")

    def delete(self, nodeID):
        temp = self.head
        while temp is not None:
            if temp.nodeID != nodeID:
                temp = temp.next
            else:
                if temp == self.head:
                    self.head = self.head.next
                    self.head.prev = None
                elif temp == self.tail:
                    self.tail = self.tail.prev
                    self.tail.next = None
                else:
                    prev = temp.prev
                    succ = temp.next
                    prev.next = succ
                    succ.prev = prev
                del temp
        print("Not Found")

    def insert(self, node):
        if(node.cost <= self.head.cost):
            self.insertAtHead(node)
        elif(node.cost>=self.tail.cost):
            self.insertAtTail(node)
        else:
            temp = self.head.next
            prev = self.head
            while(temp is not None):
                if(prev.cost <= node.cost and temp.cost >= node.cost):
                    node.next = temp
                    temp.prev = node
                    node.prev = prev
                    prev.next = node
                    break
                else:
                    temp = temp.next
                    prev = prev.next

    def __len__(self):
        i = 0
        temp = self.head
        while temp is not None:
            i+=1
            temp=temp.next
        return i


class PriorityQueue():
    def __init__(self):
        self.itemList = QueueLinkedList()

    def isEmpty(self):
        if(len(self.itemList)==0):
            return True
        return False

    def enqueue(self,nodeid,cost):
        self.itemList.insert(QueueNode(nodeid,cost))

    def dequeue(self):
        result = {self.itemList.head.nodeID : self.itemList.head.cost}
        self.itemList.delete()
        return result


