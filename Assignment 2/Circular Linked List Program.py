class Node:
    def __init__(self, name):
        self.name = name
        self.next = None

class CircularList:
    def __init__(self):
        self.head = None

    def insert(self, name):
        new = Node(name)
        if self.head is None:
            self.head = new
            new.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new
            new.next = self.head

    def delete(self, name):
        if self.head is None:
            print("List empty")
            return
        temp = self.head
        prev = None
        while True:
            if temp.name == name:
                if prev:
                    prev.next = temp.next
                else:
                    # deleting head
                    last = self.head
                    while last.next != self.head:
                        last = last.next
                    self.head = temp.next
                    last.next = self.head
                print(name, "deleted")
                return
            prev = temp
            temp = temp.next
            if temp == self.head:
                break
        print(name, "not found")

    def display(self):
        if self.head is None:
            print("List empty")
            return
        temp = self.head
        print("Patients in circular list:")
        while True:
            print(temp.name, end=" -> ")
            temp = temp.next
            if temp == self.head:
                break
        print("(back to start)")
        # --- Main Part ---
cl = CircularList()
cl.insert("Tom")
cl.insert("Jerry")
cl.display()
cl.delete("Tom")
cl.display()
