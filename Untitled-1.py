# %%
# generate permutations of a list of numbers
from itertools import permutations, combinations
# time the program
import time
# copy the board
import copy
import numpy as np
from PIL import Image
from dupe_permute import GFG

# %%
def apply_solution_to_board(arr,row=None,col=None):
    if row is not None:
        board[row] = list(arr)
    elif col is not None:
        for i in range(len(arr)):
            board[i][col] = arr[i]

# %%
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
    rs = [tuple(i) for i in res if i not in removals]
    print(res,"-",removals,"=",rs)
    return rs

# %%
def calculate_spaces(arr, wh):
    # provided an array and a width/height, return the number of spaces
    # arr = [1,2] -- [_,x,_,x,x,_,_,_,_,_]
    # wh = 10
    # return 7
    # arr = [1,2,3] -- [_,x,_,x,x_,x,x,x,_]
    # wh = 10
    # return 4
    return wh - sum(arr) - arr.count(0)

# %%
def check_arr_valid(arr):
    # Rules: arr can only be valid if every number is surrounded by 0 or -1 or the edge of the array
    # arr = [-1,1,-1,2] -- valid
    # arr = [1,1,-1] -- invalid
    for i in range(len(arr)):
        if i > 0 and arr[i] > 0 and arr[i-1] > 0:
            return False
    return True

# %%
def check_arr_solved(arr,clue):
    # eg. arr = [0,0,0,0,0,1,0,0,0,0], clue = [1], return True
    # This is a solved array, but it consists of 0s instead of -1s
    # Assuming arr is valid (it should always be valid in this instance)
    # we may count the number of 1s in arr and compare it to the clue's sum
    if sum(clue) == arr.count(1):
        arr = list(arr)
        # swap 0 with -1s
        for i in range(len(arr)):
            if arr[i] == 0:
                arr[i] = -1
    return tuple(arr)

# %%
def generate_arr(arr,wh):
    num_spaces = calculate_spaces(arr,wh)
    return arr + [0 for _ in range(num_spaces)] 

# %%
def generate_full_arr(arr):
    # provided arr, return the row/col array
    # eg. arr = [1,0,2,0] => [1,-1,1,1,-1]
    # eg. arr = [1,0,2,0,1] => [1,-1,1,1,-1,1]
    # etc.
    result = []
    for i in range(len(arr)):
        result += [1 for _ in range(arr[i])] if arr[i] > 0 else [0]
    return tuple(result)

# %%
def get_overlap(res):
    # provided a list of arrays, return the overlap:
    # this can simply be done with the sum of the arrays at each index
    # eg. res = [(1, 0, 1, 1), (1, 1, 0, 1)] => (2, 1, 1, 2)
    # if sum == len(res), then that index is a 1
    # elif sum == -len(res), then that index is a -1
    # else that index is a 0 
    print(res)
    result = [0] * len(res[0])
    for i in range(len(res)):
        for j in range(len(res[i])):
            result[j] += res[i][j]
    return tuple([1 if i == len(res) else -1 if i == -len(res) else 0 for i in result])

# %%
def get_restrictions(row=None,col=None):
    if row != None:
        return {-1: [i for i in range(len(board[row])) if board[row][i] == -1], 1: [i for i in range(len(board[row])) if board[row][i] == 1]}
    elif col != None:
        return {-1: [i for i in range(len(board)) if board[i][col] == -1], 1: [i for i in range(len(board)) if board[i][col] == 1]}

# %%
def parse_clues(path):
    # open the file
    # read the file:
    # each line is a new array of clues
    # each number is separated by a space
    # eg. 1 2 3 4 5
    # eg. 1 2 3
    with open(path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [x.split(" ") for x in content]
    content = [[int(i) for i in x] for x in content]
    return content

# %%
# Let the output be a picture of the solved board where the blocks are BLACK squares and the empty spaces are WHITE squares
# Let us define the function that will save the PNG file to output.png using the PIL library and numpy
# Save it as a 25*(len(board))x25*(len(board)) image where each pixel maps to 25x25 pixels on the board
def show_solution(b):
    board = copy.deepcopy(b)
    board = np.array(board)
    # Create a 2D array of 0s with the same size as the board
    # output is initialized with #CD853F (PERU) as the background color and #800000 (MAROON) as the block color
    color_map = {
        0: (0, 0, 0),
        1: (205, 133, 63),
        -1: (128, 0, 0)
    }

    # Determine the size of the output image
    len_input = board.shape[0]
    output_size = (25 * len_input, 25 * len_input)

    # Create the output image
    output_image = Image.new('RGB', output_size)

    # Draw squares for each value in the input array
    for i in range(len_input):
        for j in range(len_input):
            color = color_map[board[j, i]]
            square = (i * 25, j * 25, (i + 1) * 25, (j + 1) * 25)
            output_image.paste(color, square)
    # Save the output as a PNG file
    output_image.save('output.png')


# %%
def solve_picross():
    old_board = copy.deepcopy(board)
    while True:
        # solve the rows
        for i in range(len(row_clues)):
            gfg = GFG()
            # generate all possible permutations of the row
            gfg.nums = generate_arr(row_clues[i],width)
            perms = gfg.getDistinctPermutations()
            # remove the invalid permutations
            perms = [i for i in perms if check_arr_valid(i)]
            # get the restrictions
            restrictions = get_restrictions(row=i)
            # get the full array
            perms = [generate_full_arr(i) for i in sorted(perms)]
            # apply the restrictions
            perms = apply_restrictions(perms, restrictions)
            # get the overlap
            overlap = get_overlap(perms)
            print(overlap,row_clues[i],"at row",i)
            # check if the overlap solves the row
            sol = check_arr_solved(overlap,row_clues[i])
            print(sol)
            # apply the sol to the board
            apply_solution_to_board(sol,row=i)
            print(len(board), [len(i) for i in board], "\n", board)
        
        # solve the cols
        for i in range(len(col_clues)):
            # generate all possible permutations of the col
            gfg.nums = generate_arr(col_clues[i], width)
            perms = gfg.getDistinctPermutations()
            # remove the invalid permutations
            perms = [i for i in perms if check_arr_valid(i)]
            # get the restrictions
            restrictions = get_restrictions(col=i)
            # get the full array
            perms = [generate_full_arr(i) for i in sorted(perms)]
            # apply the restrictions
            perms = apply_restrictions(perms, restrictions)
            # get the overlap
            overlap = get_overlap(perms)
            print(overlap, col_clues[i], "at col", i)
            # check if the overlap solves the col
            sol = check_arr_solved(overlap, col_clues[i])
            print(sol)
            # apply the sol to the board
            apply_solution_to_board(sol, col=i)
            print(len(board), [len(i) for i in board], "\n", board)
        # check if the board has changed
        has_changed = False
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != old_board[i][j]:
                    has_changed = True
        if not has_changed:
            break
        print(board)
        old_board = copy.deepcopy(board)

# %%
# balloon
row_clues = parse_clues("row_clues.txt")
col_clues = parse_clues("col_clues.txt")

# %%
print(row_clues)
print(col_clues)

# %%
# ship
# row_clues = [[1], [7], [5], [5], [5], [7], [1], [10], [9], [7]]
# col_clues = [[1], [2], [1, 1, 3], [5, 3], [
#     5, 3], [10], [5, 3], [5, 3], [1, 1, 3], [2]]

width = len(col_clues)
height = len(row_clues)
board = [[0 for _ in range(width)] for _ in range(height)]

print(len(board),[len(i) for i in board],"\n",board)

# %%


# %%
solve_picross()


# %%
show_solution(board)


