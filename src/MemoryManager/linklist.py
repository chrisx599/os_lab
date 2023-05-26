from Memory import *
class Node:
    value = 0
    next = None


class linklist:
    head = None

    def __init__(self):
        self.head = Node()

    def get_length(self):
        count = 0
        cur_node = self.head
        while (cur_node != None):
            count = count + 1
            cur_node = cur_node.next
        return count

    def insert_head(self, value):
        new_node = Node()
        new_node.value = value
        new_node.next = self.head
        self.head = new_node

    def insert_tail(self, value):
        new_node = Node()
        new_node.value = value
        cur_node = self.head
        while (cur_node.next != None):
            cur_node = cur_node.next
        cur_node.next = new_node
        new_node.next = None

    def search_value(self, value):
        cur_node = self.head
        count = 0
        while (cur_node != None):
            if (cur_node.value == value):
                return count + 1
            cur_node = cur_node.next
            count = count + 1
        return 0