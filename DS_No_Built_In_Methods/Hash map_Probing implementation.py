from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    @staticmethod
    def _is_active(entry: HashEntry) -> bool:
        """Determine if given entry is not a tombstone."""
        return entry and not entry.is_tombstone

    def _quad_probe(self, key: str) -> int:
        """Return index of empty position, or position matching given key."""
        # quadratic probing scheme from "Data Structures & Algorithms using Java"
        # by Mark Allen Weiss
        offset = 1
        index = self._hash_function(key) % self._capacity

        # search table until empty spot or match
        while self._buckets[index]:

            if self._buckets[index].key == key:
                return index

            # can use fast addition and subtraction
            # as opposed to multiplication and division
            index += offset
            offset += 2
            if index >= self._buckets.length():
                index -= self._buckets.length()

        return index

    def _module_quad_probe(self, key: str) -> int:
        """Return index of empty position, or position matching given key."""
        # quadratic probing formula based on module
        increment = 1
        initial_index = index = self._hash_function(key) % self._capacity
        while self._buckets[index]:

            if self._buckets[index].key == key:
                return index

            # students often make the mistake of using a single variable
            # the initial index is separate from the moving index
            index = (initial_index + increment ** 2) % self._capacity
            increment += 1

        return index

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        """
        # resize if the table is too full
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        index = self._quad_probe(key)

        # don't increment size if overwriting a value
        if self._is_active(self._buckets[index]):
            self._buckets[index].value = value
            return

        # can check if is a tombstone and reset values,
        # or just create a new entry like
        self._buckets[index] = HashEntry(key, value)
        self._size += 1

    def table_load(self) -> float:
        """
        TODO: Write this implementation
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        TODO: Write this implementation
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        # since there's no linked list in this version,
        # the new_capacity can't be smaller than the current number of elements
        if new_capacity < self._size:
            return

        # store existing hash map content
        old_buckets = self._buckets
        old_capacity = self._capacity

        # students will likely run into difficulty if they call clear(),  #
        # instead of manually resetting (like below).                     #

        # replace current content with clear DA of new capacity
        # and make sure the capacity is a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity

        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

        for i in range(old_capacity):

            # rehash non-deleted entry in new table
            current_entry = old_buckets[i]
            if self._is_active(current_entry):
                self.put(current_entry.key, current_entry.value)

    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        """
        index = self._quad_probe(key)
        if self._is_active(self._buckets[index]):
            return self._buckets[index].value

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        index = self._quad_probe(key)

        # if already a tombstone, do nothing
        if self._is_active(self._buckets[index]):
            self._buckets[index].is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        # append()ing None may cause problems
        for i in range(self._capacity):
            self._buckets[i] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        result = DynamicArray()
        for i in range(self._capacity):
            entry = self._buckets[i]
            if self._is_active(entry):
                result.append((entry.key, entry.value))

        return result

    # possible solution to iterator problem uses
    # an iterator that's part of the class
    def __iter__(self):
        """
        TODO: Write this implementation
        """
        # same as Bag's __iter__()
        self.index = 0
        return self

    def __next__(self):
        """
        TODO: Write this implementation
        """
        # handles None and tombstone entries
        try:
            while self._buckets[self.index] is None or self._buckets[self.index].is_tombstone is True:
                self.index += 1
        except DynamicArrayException:
            raise StopIteration

        # handles the index being greater than the length of the dynamic array
        # same as Bag's __next__(), as they share the same underlying data structure
        try:
            value = self._buckets[self.index]
        except DynamicArrayException:
            raise StopIteration
        self.index += 1

        return value

    # another possible solution to the iterator problem uses
    # the iterator defined here, and the separate class below.
    # either one is acceptable
    '''
    def __iter__(self):
        return HashMapIterator(self._buckets)


class HashMapIterator(object):
    def __init__(self, da):
        self.index = 0
        self.da = da

    def __iter__(self):
        return self

    # same as built-in __next__
    def __next__(self):
        try:
            while self.da[self.index] is None or self.da[self.index].is_tombstone is True:
                self.index += 1
        except DynamicArrayException:
            raise StopIteration

        try:
            value = self.da[self.index]
        except DynamicArrayException:
            raise StopIteration
        self.index += 1

        return value
    '''


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
