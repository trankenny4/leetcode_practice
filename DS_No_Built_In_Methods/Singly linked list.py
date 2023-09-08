from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initializes a new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """Insert new node at front of list."""

        # old head's next becomes new head's next
        self._head.next = SLNode(value, self._head.next)

    def insert_back(self, value: object) -> None:
        """Insert new node at the end of the list."""

        node = self._head
        while node.next:
            node = node.next

        # node.next is None; put a node there
        node.next = SLNode(value)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Insert the given value at the desired index.
        Index 0 is first node after head.
        """
        if index < 0 or index > self.length():
            raise SLLException

        node = self._head
        for _ in range(index):
            node = node.next

        node.next = SLNode(value, node.next)

        # alternate approach #1
        # temp = node.next
        # node.next = SLNode(value)
        # node.next.next = temp

        # alternate approach #2
        # new_node = SLNode(value)
        # new_node.next = node.next
        # node.next = new_node

    def remove_at_index(self, index: int) -> None:
        """
        Attempt to remove node at desired index.
        Index 0 is first node after head.
        """
        if index < 0 or index >= self.length():
            raise SLLException

        node = self._head
        for _ in range(index):
            node = node.next

        node.next = node.next.next

    def remove(self, value: object) -> bool:
        """
        Attempt to remove given value from list.
        Report success of the removal as a boolean value.
        """
        node = self._head

        # maintain pointer 1 away,
        while node.next:

            # so removal by pointing past current node can happen
            if node.next.value == value:
                node.next = node.next.next
                return True

            node = node.next

        return False

    def count(self, value: object) -> int:
        """Count number of occurrences of given value found in list."""

        count = 0
        node = self._head.next
        while node:
            if node.value == value:
                count += 1
            node = node.next
        return count

    def find(self, value: object) -> bool:
        """
        Find the given value in the list and returns its success or failure.
        """
        node = self._head.next
        while node:
            if node.value == value:
                return True
            node = node.next
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        Attempt to return a new LinkedList of the desired size,
        starting at the given index.
        Index 0 is first node after head.
        """

        if start_index < 0 or size < 0:
            raise SLLException

        length = self.length()

        if start_index >= length or start_index + size > length:
            raise SLLException

        if size == 0:
            return LinkedList()

        # move through list, find node where slicing will begin
        node = self._head.next
        for _ in range(start_index):
            node = node.next

        # create new list and get a node reference
        slice_list = LinkedList()
        slice_node = slice_list._head

        # add new node to slice_list and move forward through both lists
        for _ in range(size):
            slice_node.next = SLNode(node.value)
            slice_node = slice_node.next
            node = node.next

        return slice_list


if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")
