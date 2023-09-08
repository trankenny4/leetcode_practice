from dynamic_array_solution import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da[_])
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> (DynamicArray, int):
        """
        TODO: Write this implementation
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        TODO: Write this implementation
        """
        for i in range(self._da.length()):
            if self._da[i] == value:
                self._da.remove_at_index(i)
                return True
        return False

    def count(self, value: object) -> int:
        """
        TODO: Write this implementation
        """
        count = 0
        for i in range(self._da.length()):
            count += self._da[i] == value
        return count

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        self._da = DynamicArray()

    def equal(self, second_bag: "Bag") -> bool:
        """
        TODO: Write this implementation
        """
        for i in range(self._da.length()):
            item = self._da[i]
            if self.count(item) != second_bag.count(item):
                return False

        for i in range(second_bag._da.length()):
            item = second_bag._da[i]
            if self.count(item) != second_bag.count(item):
                return False

        return True

    # Possible solution to iterator problem uses
    # an iterator that's part of the class
    '''
    def __iter__(self):
        """"""
        self.index = 0
        return self
    def __next__(self):
        """"""
        try:
            value = self._da[self.index]
        except DynamicArrayException:
            raise StopIteration
        self.index += 1
        return value
    '''

    # Another possible solution to iterator problem uses
    # the iterator defined here
    def __iter__(self):
        """"""
        return Bag_Iterator(self._da)

# And a separate class. Either one is acceptable
class Bag_Iterator(object):
    def __init__(self, dyn_array):
        self.index = 0
        self.dyn_array = dyn_array

    def __iter__(self):
        return self

    # Use this for built-in iteration
    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        if self.index >= self.dyn_array.length():
            raise StopIteration
        value = self.dyn_array.get_at_index(self.index)

        self.index = self.index + 1
        return value

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)
