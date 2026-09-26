import time
import random
import threading

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def parallel_quick_sort(arr, low, high, num_threads):
    if low < high:
        pivot_index = partition(arr, low, high)

        if num_threads > 1:
            left_threads = num_threads // 2
            right_threads = num_threads - left_threads

            left_thread = threading.Thread(target=parallel_quick_sort, args=(arr, low, pivot_index - 1, left_threads))
            left_thread.start()

            parallel_quick_sort(arr, pivot_index + 1, high, right_threads)
            left_thread.join()
        else:
            parallel_quick_sort(arr, low, pivot_index - 1, num_threads=1)
            parallel_quick_sort(arr, pivot_index + 1, high, num_threads=1)


def benchmark(size, threads=1):
    arr = [random.randint(0, 100000) for _ in range(size)]
    start = time.perf_counter()
    parallel_quick_sort(arr, 0, len(arr) - 1, threads)
    return time.perf_counter() - start


sizes = [100, 1000, 10000, 20000, 30000, 40000, 50000]
print(f"{'Размер'} | {'БС '} | {'БС_П 2'} | {'БС_П 4'} | {'БС_П 8'}")
print("-" * 58)

for size in sizes:
    t1 = benchmark(size, 1)
    t2 = benchmark(size, 2)
    t4 = benchmark(size, 4)
    t8 = benchmark(size, 8)
    print(f"{size} | {t1} | {t2} | {t4} | {t8}")