
# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------

def min_max(arr: StaticArray) -> tuple[int, int]:
    """
    Return a tuple containing the minimum
    and maximum values found in the input array.
    """
    # must be O(n)

    min_value = max_value = arr[0]

    for i in range(1, arr.length()):

        current_value = arr[i]

        if current_value < min_value:
            min_value = current_value

        elif current_value > max_value:
            max_value = current_value

    return min_value, max_value


# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------

def fizz_buzz(arr: StaticArray) -> StaticArray:
    """Return an array adhering to the "fizzbuzz" criteria."""

    # must be O(n)

    length = arr.length()
    result = StaticArray(length)

    for i in range(length):

        current_value = arr[i]

        if current_value % 15 == 0:
            result[i] = 'fizzbuzz'
        elif current_value % 5 == 0:
            result[i] = 'buzz'
        elif current_value % 3 == 0:
            result[i] = 'fizz'
        else:
            result[i] = current_value

    return result


# ------------------- PROBLEM 3 - REVERSE -----------------------------------

def reverse(arr: StaticArray) -> None:
    """Reverse the given array."""

    # must be O(n)

    start, end = 0, arr.length() - 1

    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1


# ------------------- PROBLEM 4 - ROTATE ------------------------------------

def rotate(arr: StaticArray, steps: int) -> StaticArray:
    """
    Return new array that contains the same content as the
    input array, except the elements are shifted over steps times;
    positive steps to the right, negative steps to the left
    """
    # must be O(n)

    size = arr.length()
    result = StaticArray(size)

    # steps % size is the starting index for the rotation.
    # incrementing with the loop variable (src) gets the
    # very next index (1 to the right, or wrap-around to index 0)

    for src in range(size):
        result[(src + steps) % size] = arr[src]

    return result


# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------

def sa_range(start: int, end: int) -> StaticArray:
    """
    Return an array that contains all consecutive integers
    between start and end (inclusive).
    """
    # must be O(n)

    size = abs(end - start) + 1
    result = StaticArray(size)

    # step is positive if incrementing, negative if decrementing
    step = 1 if start < end else -1

    # start + step is the ticket
    value = start
    for i in range(size):
        result[i] = value
        value += step

    # previous solution
    # for i, value in enumerate(range(start, end + step, step)):
    #    result[i] = value

    return result


# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------

def is_sorted(arr: StaticArray) -> int:
    """
    Determine if input array is sorted.
    Return 1 if sorted in strictly ascending order;
    return -1 if sorted in strictly descending order;
    0 otherwise.
    """
    # must be O(n)

    asc_flag = des_flag = True
    i = 1

    # use variable instead of calling length() every iteration
    # (for loops only call length() once)
    length = arr.length()

    while i < length and (asc_flag or des_flag):

        value_on_right = arr[i]
        value_on_left = arr[i - 1]

        if value_on_right < value_on_left:
            asc_flag = False
        elif value_on_right > value_on_left:
            des_flag = False

        # if they're equal, then not strictly ascending or descending
        else:
            return 0

        i += 1

    # more likely to see something like this?
    # if asc_flag:
    #    return 1
    # if des_flag:
    #    return -1
    # return 0

    # black magic
    return 1 if asc_flag else -1 if des_flag else 0


# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------
def find_mode(arr: StaticArray) -> tuple[object, int]:
    """
    Return a tuple containing the mode and
    its frequency from the given array.
    """

    # starting mode and its frequency
    mode, frequency = arr[0], 1
    current_frequency = 1

    for i in range(arr.length() - 1):

        if arr[i] == arr[i + 1]:
            current_frequency += 1
        else:
            current_frequency = 1

        if current_frequency > frequency:
            mode = arr[i]
            frequency = current_frequency

    return mode, frequency


def _alternate_find_mode(arr: StaticArray) -> (int, int):
    """
    Grigori Barbachov's legacy solution.
    """
    # must be O(n) and with
    # no additional StaticArrays created

    # starting mode and its frequency
    mode, frequency = arr[0], 1

    i, end = 0, arr.length() - 1
    while i < end:

        new_frequency = 1

        # still O(n) since i is progressed in this loop
        while i < end and arr[i] == arr[i + 1]:
            new_frequency += 1
            i += 1

        # found new mode?
        if new_frequency > frequency:
            frequency = new_frequency
            mode = arr[i]

        i += 1

    return mode, frequency


# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------

def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    Given a sorted array, return a new array containing
    only the unique values from the input array
    """
    # must be O(n)

    # determine size of output array by counting number of unique values
    result_size = input_arr_length = arr.length()
    for i in range(1, input_arr_length):
        result_size -= 1 if arr[i] == arr[i - 1] else 0

    # create and fill output array of unique values
    result = StaticArray(result_size)
    result[0] = arr[0]
    dst = 1
    for src in range(1, input_arr_length):
        if arr[src] != arr[src - 1]:
            result[dst] = arr[src]
            dst += 1

    return result


# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------

def count_sort(arr: StaticArray) -> StaticArray:
    """The fabled count sort. Sorts in non-ascending order."""

    # must be O(n + k)

    # find minimum and maximum values in the array
    min_value, max_value = min_max(arr)

    # create array and initialize all counts to 0
    count_length = max_value - min_value + 1
    counts = StaticArray(count_length)
    for i in range(count_length):
        counts[i] = 0

    # keep counts of each value in the original input
    input_arr_length = arr.length()
    for i in range(input_arr_length):
        counts[arr[i] - min_value] += 1

    # create sorted output array
    result = StaticArray(input_arr_length)
    dst = input_arr_length - 1
    for i in range(count_length):
        count = counts[i]
        value = i + min_value
        for j in range(count):
            result[dst] = value
            dst -= 1

    return result


# ------------------- PROBLEM 10 - SORTED SQUARES ---------------------------

def sorted_squares(arr: StaticArray) -> StaticArray:
    """
    Given an array sorted in non-descending order, returns a new array
    filled with squares of the values from the input array
    """
    # must be O(n)

    length = arr.length()
    result = StaticArray(length)

    # since result will always be positive,
    # fill up end of array with larger value and work towards the front
    front, back = 0, length - 1
    for i in range(length - 1, -1, - 1):

        if abs(arr[front]) > abs(arr[back]):
            result[i] = arr[front] ** 2
            front += 1
        else:
            result[i] = arr[back] ** 2
            back -= 1

    return result


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]: 3}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        result = min_max(arr)
        if result:
            print(f"Min: {result[0]: 3}, Max: {result[1]}")
        else:
            print("min_max() not yet implemented")

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-95, -89), (-89, -95)]
    for start, end in cases:
        print(f"Start: {start: 4}, End: {end: 4}, {sa_range(start, end)}")

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = is_sorted(arr)
        space = "  " if result and result >= 0 else " "
        print(f"Result:{space}{result}, {arr}")

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value

        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        before = arr if len(case) < 50 else 'Started sorting large array'
        print(f"Before: {before}")
        result = count_sort(arr)
        after = result if len(case) < 50 else 'Finished sorting large array'
        print(f"After : {after}")

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')
