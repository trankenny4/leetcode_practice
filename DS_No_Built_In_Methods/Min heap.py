# two methods (swap() and pop()) are added to this DA
from dynamic_array_solution import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """Add new node to the heap."""

        # add element at end and percolate it up
        self._heap.append(node)
        self._percolate_up(self._heap.length() - 1)

    def _percolate_up(self, index: int) -> None:
        """Percolate up given node to correct heap position."""

        # repeat until reached beginning of array
        while index > 0:
            # compute element's parent index
            parent = (index - 1) // 2

            # is value at parent index > percolating element?
            if self._heap[parent] > self._heap[index]:
                self._heap.swap(parent, index)

            # repeat with next parent until beginning of array
            index = parent

    def is_empty(self) -> bool:
        """Return True if no elements in the heap, False otherwise."""
        return self._heap.length() == 0

    def get_min(self) -> object:
        """
        Return value of top node without removing it.
        Raises MinHeapException if heap is empty.
        """
        if self.is_empty():
            raise MinHeapException
        return self._heap[0]

    def remove_min(self) -> object:
        """
        Remove top node from the heap and return it.
        Raise MinHeapException if heap is empty.
        """
        if self.is_empty():
            raise MinHeapException

        # edge case of single element heap
        if self._heap.length() == 1:
            return self._heap.pop()

        # store deleted deleted node for return later
        removed_node = self._heap[0]

        # replace root with rightmost bottom leaf
        self._heap[0] = self._heap.pop()

        # percolate down root node, observing heap rules
        _percolate_down(self._heap, 0)
        return removed_node

    def build_heap(self, da: DynamicArray) -> None:
        """Create a heap from given DA and replace current heap contents."""

        # cannot just set self._heap = da
        # because then they will refer to the same object in memory
        # a deep copy is needed
        self._heap = DynamicArray()
        for i in range(da.length()):
            self._heap.append(da[i])

        # make it a proper heap
        _heapify(self._heap)

    def size(self) -> int:
        """Return the number of items stored in the heap."""
        return self._heap.length()

    def clear(self) -> None:
        """Clear the contents of the heap."""
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """Sort given dynamic array in non-ascending order using a heapsort."""

    # need to build heap in place, can't create another DA or MinHeap
    _heapify(da)

    # loop backwards to 0
    # can stop as soon as k equals 0,
    # since you would be swapping at index 0 with index 0
    for k in range(da.length() - 1, 0, -1):

        # swap first element (min) with last element at index k
        da.swap(0, k)

        # percolate, stop before k
        _percolate_down(da, 0, k)


def _heapify(da: DynamicArray) -> None:
    """Create a proper heap from given DA"""

    # percolate down all non-leaf nodes in reverse order
    start = da.length() // 2 - 1
    for i in range(start, -1, -1):
        _percolate_down(da, i)

def _percolate_down(da: DynamicArray, parent: int, stop=None) -> None:
    """Percolate down given node to correct heap position."""

    N = da.length() if stop is None else stop

    while 0 <= parent < N:
        swap_child = None
        left_index = 2 * parent + 1
        right_index = 2 * parent + 2

        # 2 children: if right child exists, so does left
        if right_index < N and da[right_index] < da[parent]:
            # swap with the lesser of two children, swap with left if equal
            swap_child = left_index if da[left_index] <= da[right_index] else right_index

        # 1 child: if left child is less than parent, swap with left child
        elif left_index < N and da[left_index] < da[parent]:
            swap_child = left_index

        if swap_child is None:
            return

        # continue down tree if swap occurred
        da.swap(parent, swap_child)
        parent = swap_child


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)
