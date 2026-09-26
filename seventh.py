class Tree: # для первого задания
    def __init__(self, left, right, val): 
        self.left = left
        self.right = right
        self.val = val


def trees_number_two(tree):
    def rec(f, s):
        if f is None and s is None:
            return True
        if f is None or s is None:
            return False

        if f.val != s.val:
            return False

        return rec(f.right, s.left) and rec(f.left, s.right)

    if tree.left is None and tree.right is None:
        return True
    if (tree.left is None and tree.right is not None) or (tree.right is None and tree.left is not None):
        return False
    
    return rec(tree.left, tree.right)


def greedy_number_six():
    m = int(input())
    input()
    values = list(map(int, input().split()))
    
    methods = [0] * (m + 1)
    methods[0] = 1  

    for coin in values:
        for i in range(coin, m + 1):
            methods[i] += methods[i - coin]

    print(methods[-1])


def split_and_reign_number_one(arr): # сильно сомневаюсь, что "разделяй и влавствуй" переводится именно так, но ничего лучше в голову не пришло
    def split_arr_get_min_max(start, end, arr):
        if start == end:
            return arr[start], arr[end]

        if start + 1 == end:
            if arr[start] > arr[end]:
                return arr[end], arr[start]
            return arr[start], arr[end]

        middle = (start + end) // 2

        left_min, left_max = split_arr_get_min_max(start, middle, arr)
        right_min, right_max = split_arr_get_min_max(middle + 1, end, arr)

        if left_min < right_min:
            res_min = left_min
        else:
            res_min = right_min

        if left_max > right_max:
            res_max = left_max
        else:
            res_max = right_max

        return res_min, res_max

    return split_arr_get_min_max(0, len(arr) - 1, arr)


def search_with_backtrack():
    n = int(input())

    def backtrack(current_state, needed):
        if sum(current_state) == needed:
            print(*current_state)
            return

        if sum(current_state) > needed:
            return

        for i in range(current_state[-1], needed + 1):
            new_state = current_state[:]
            new_state.append(i)
            backtrack(new_state, needed)


    for i in range(1, n + 1):
        backtrack([i], n)





        

        
        
