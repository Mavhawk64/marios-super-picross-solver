# generate permutations of a list of numbers
from itertools import permutations, combinations
# time the program
import time

board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

width = len(board)

def apply_solution_to_board(arr,row=None,col=None):
    if row is not None:
        board[row] = list(arr)
    elif col is not None:
        for i in range(len(arr)):
            board[i][col] = arr[i]


def apply_restrictions(res, dct):
    # provided a list of arrays and a dictionary of restrictions, remove the invalid arrays and return the new list
    # eg. res = [(1, 0, 1, 1), (1, 1, 0, 1)] and dct = {-1: [1], 1: []} -> this means that there can only be a -1 at index 1 (if it is 0, then rewrite to -1. if it is 1, remove the list)
    removals = []
    res = [list(i) for i in res]
    for i in range(len(res)):
        for k in dct[-1]:
            if res[i][k] == 0 or res[i][k] == -1:
                res[i][k] = -1
            else:
                removals.append(res[i])
        for k in dct[1]:
            if res[i][k] != 1:
                removals.append(res[i])
    return [tuple(i) for i in res if i not in removals]

def calculate_spaces(arr, wh):
    # provided an array and a width/height, return the number of spaces
    # arr = [1,2] -- [_,x,_,x,x,_,_,_,_,_]
    # wh = 10
    # return 7
    # arr = [1,2,3] -- [_,x,_,x,x_,x,x,x,_]
    # wh = 10
    # return 4
    return wh - sum(arr)

def check_arr_valid(arr):
    # Rules: arr can only be valid if every number is surrounded by 0 or -1 or the edge of the array
    # arr = [-1,1,-1,2] -- valid
    # arr = [1,1,-1] -- invalid
    for i in range(len(arr)):
        if i > 0 and arr[i] > 0 and arr[i-1] > 0:
            return False
    return True

def generate_arr(arr,wh):
    num_spaces = calculate_spaces(arr,wh)
    return arr + [0 for _ in range(num_spaces)] 

def generate_full_arr(arr):
    # provided arr, return the row/col array
    # eg. arr = [1,0,2,0] => [1,-1,1,1,-1]
    # eg. arr = [1,0,2,0,1] => [1,-1,1,1,-1,1]
    # etc.
    result = []
    for i in range(len(arr)):
        result += [1 for _ in range(arr[i])] if arr[i] > 0 else [0]
    return tuple(result)

def get_overlap(res):
    # provided a list of arrays, return the overlap:
    # this can simply be done with the sum of the arrays at each index
    # eg. res = [(1, 0, 1, 1), (1, 1, 0, 1)] => (2, 1, 1, 2)
    # if sum == len(res), then that index is a 1
    # elif sum == -len(res), then that index is a -1
    # else that index is a 0 
    result = [0] * len(res[0])
    for i in range(len(res)):
        for j in range(len(res[i])):
            result[j] += res[i][j]
    return tuple([1 if i == len(res) else -1 if i == -len(res) else 0 for i in result])

# start the timer
start = time.time()

result = list(permutations(generate_arr([1,2],4)))

print(len(result))
# remove duplicates
result = list(set([tuple(i) for i in result]))
print(len(result))
# remove invalid arrays
result = [i for i in result if check_arr_valid(i)]
print(len(result))
print(sorted(result))
rizz = [generate_full_arr(i) for i in sorted(result)]

print(rizz)

restricted = apply_restrictions(rizz, {-1: [], 1: [0, 3]})

print(restricted)

overlap = get_overlap(restricted)

print(overlap)

apply_solution_to_board(arr=overlap, row=None, col=1)

print(board)

# end the timer
end = time.time()

# print the timer in seconds
print("[Finished in",end - start,"seconds]")
