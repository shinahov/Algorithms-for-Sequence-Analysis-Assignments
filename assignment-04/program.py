import sys
import math


def better(array, index1, index2):
    if index1 is None:
        return index2
    if index2 is None:
        return index1

    if array[index1] < array[index2]:
        return index1
    if array[index1] > array[index2]:
        return index2

    return min(index1, index2)


def sparse_query(array_a, table, left, right):
    length = right - left

    if length <= 0:
        return None

    power = 2 ** int(math.floor(math.log2(length)))

    # index of min from left interval and right interval
    j1 = table[(left, left + power)]
    j2 = table[(right - power, right)]

    if array_a[j1] <= array_a[j2]:
        return j1
    else:
        return j2


def rmq_query(array, i, j, block_size, p_array, a_array, sparse_table):
    if i > j:
        i, j = j, i

    left_block = i // block_size
    right_block = j // block_size

    best = None

    if left_block == right_block:
        for k in range(i, j + 1):
            best = better(array, best, k)
        return best

    left_end = min((left_block + 1) * block_size - 1, len(array) - 1)

    for k in range(i, left_end + 1):
        best = better(array, best, k)

    right_start = right_block * block_size

    for k in range(right_start, j + 1):
        best = better(array, best, k)

    middle_left = left_block + 1
    middle_right = right_block

    middle_block = sparse_query(a_array, sparse_table, middle_left, middle_right)

    if middle_block is not None:
        real_index = p_array[middle_block]
        best = better(array, best, real_index)

    return best


def get_min(array, offset):
    # get min for an block, O(n)
    min_index = 0

    for i in range(1, len(array)):
        if array[i] < array[min_index]:
            min_index = i
    return offset + min_index, array[min_index]


def build_a_and_p_array(array, block_size):
    # get min for each block, O(n)

    p_array = []
    a_array = []

    for start in range(0, len(array), block_size):
        block = array[start : start + block_size]

        index, value = get_min(block, start)
        p_array.append(index)
        a_array.append(value)
    return p_array, a_array


def build_sparce_table(array_a):
    table = dict()
    # add length -1 intervals to table
    for i in range(0, len(array_a)):
        table[(i, i + 1)] = i

    length = 2
    # add longer intervals
    while length <= len(array_a):
        half = length // 2

        for i in range(0, len(array_a) - length + 1):
            j1 = table[(i, i + half)]
            j2 = table[(i + half, i + length)]

            if array_a[j1] <= array_a[j2]:
                table[(i, i + length)] = j1
            else:
                table[(i, i + length)] = j2

        length *= 2

    return table


filename = sys.argv[1]
i = int(sys.argv[2])
j = int(sys.argv[3])

with open(filename, "r") as file:
    input = list(map(int, file.read().strip().split(",")))


block_size = math.ceil(math.log2(len(input)) / 2)
p_array, a_array = build_a_and_p_array(input, block_size)


table = build_sparce_table(array_a=a_array)


result_index = rmq_query(input, i, j, block_size, p_array, a_array, table)
print("Sparse Table")
print("Index Range   Index Range")


for key in sorted(table.keys(), key=lambda x: (x[1] - x[0], x[0])):
    start, end = key
    print(f"{start} to {end}        {table[key]}")

print("\n")
print("Array P")
print(p_array)
print("\n")
print("Output")
print(f"{input[result_index]},{result_index}")
