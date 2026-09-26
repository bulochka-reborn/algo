import random
import unittest
import time

def insert_sort(arr):
    for i in range(1, len(arr)):
        j = i - 1
        k = arr[i]

        while j >= 0 and k < arr[j]:
            arr[j + 1] = arr[j]
            j = j - 1

        arr[j + 1] = k


def radix_sort(arr):
    def sort_for_radix(current_arr, n):  # нейминг переменных - самое больное
        buckets = [[] for _ in range(10)]

        for num in current_arr:
            num_str = str(num).zfill(n_radix)

            digit_index = -1 - n
            digit = int(num_str[digit_index])

            buckets[digit].append(num)

        res = []

        for bucket in buckets:
            res.extend(bucket)

        return res

    n_radix = len(str(max(arr)))

    for i in range(n_radix):
        arr = sort_for_radix(arr, i)

    return arr


def quick_sort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)

        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1

            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


class SortingTest(unittest.TestCase):
    def test_sorting_time(self):
        lengths = (10000, 12000, 14000, 16000, 18000, 20000)
        times = [[], [], []]

        for length in lengths:
            print(length)

            array = list(range(length))
            random.shuffle(array)

            time_start = time.perf_counter()
            quick_sort(array[:], 0, len(array) - 1)
            time_end = time.perf_counter()
            times[0].append(time_end - time_start)

            time_start = time.perf_counter()
            radix_sort(array[:])
            time_end = time.perf_counter()
            times[1].append(time_end - time_start)

            time_start = time.perf_counter()
            insert_sort(array[:])
            time_end = time.perf_counter()
            times[2].append(time_end - time_start)
