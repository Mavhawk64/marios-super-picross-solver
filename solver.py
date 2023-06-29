import copy
import numpy as np
from PIL import Image

# Let the output be a picture of the solved board where the blocks are BLACK squares and the empty spaces are WHITE squares
# Let us define the function that will save the PNG file to output.png using the PIL library and numpy
# Save it as a 25*(len(board))x25*(len(board)) image where each pixel maps to 25x25 pixels on the board
def show_solution(b):
    board = copy.deepcopy(b)
    board = np.array(board)
    # Create a 2D array of 0s with the same size as the board
    # output is initialized with #CD853F (PERU) as the background color and #800000 (MAROON) as the block color
    color_map = {
        0: (0,0,0),
        1: (205, 133, 63),
        2: (128, 0, 0)
    }

    # Determine the size of the output image
    len_input = board.shape[0]
    output_size = (25 * len_input, 25 * len_input)

    # Create the output image
    output_image = Image.new('RGB', output_size)

    # Draw squares for each value in the input array
    for i in range(len_input):
        for j in range(len_input):
            color = color_map[board[i,j]]
            square = (i * 25, j * 25, (i + 1) * 25, (j + 1) * 25)
            output_image.paste(color, square)
    # Save the output as a PNG file
    output_image.save('output.png')

# Let us define the function that will find the trivial solutions
# The function will take in the board, the horizontal array, and the vertical array
# The function will return the board with the trivial solutions filled in
def find_trivial(b, hort, vert):
    board = copy.deepcopy(b)
    # First, find if there are any [0] elements inside the hort/vert arrays
    # If there are, then fill in the entire row/column with EMPTY
    for i in range(len(hort)):
        if hort[i] == [0]:
            for j in range(len(hort)):
                board[i][j] = 2
    for i in range(len(vert)):
        if vert[i] == [0]:
            for j in range(len(vert)):
                board[j][i] = 2
    
    # Next, find if there are any [len(board)] elements inside the hort/vert arrays
    # If there are, then fill in the entire row/column with BLOCK
    for i in range(len(hort)):
        print(hort[i] == [len(board)])
        if hort[i] == [len(board)]:
            for j in range(len(hort)):
                board[i][j] = 1
    for i in range(len(vert)):
        if vert[i] == [len(board)]:
            for j in range(len(vert)):
                board[j][i] = 1
    
    # Next, find if there are any hort/vert arrays that add up to len(board) including the spaces between the blocks
    # This one is a bit more complicated because we have to find the number of spaces between the blocks
    # However, we can calculate the [min] number of spaces between the blocks by counting len(board[elem]) - 1
    # For example: [1,13] is trivial for a 15x15 board because there is a sum of 14 + 1 space block = 15
    #              [9,3,1] is trivial for a 15x15 board because there is a sum of 13 + 2 space blocks = 15
    #              [1,1,1,1,1,1,1,1] is trivial for a 15x15 board because there is a sum of 8 + 7 space blocks = 15
    for i in range(len(hort)):
        if sum(hort[i]) + len(hort[i]) - 1 == len(board):
            for j in range(len(hort[i])):
                for k in range(hort[i][j]):
                    board[i][k + sum(hort[i][0:j]) + j] = 1
                if hort[i][j] != len(board):
                    board[i][hort[i][j]] = 2
    
    for i in range(len(vert)):
        if sum(vert[i]) + len(vert[i]) - 1 == len(board):
            for j in range(len(vert[i])):
                for k in range(vert[i][j]):
                    board[k + sum(vert[i][0:j]) + j][i] = 1
                if vert[i][j] != len(board):
                    board[vert[i][j]][i] = 2
    
    return board

# Let us define the function that will find the possible solutions for each row/column by viewing the large elements (i.e. the elements that are greater than len(board)/2)
# The function will take in the board, the horizontal array, and the vertical array
# The function will return the board with the possible solutions filled in
def find_large(b, hort, vert):
    board = copy.deepcopy(b)
    # First, let us find the possible solutions for each row by viewing the large elements
    # For example: [8] consists of a large element for a 10x10 board because 8 > 10/2, and thus we can do the following operation:
    # Count down the row/column 8 blocks. Mark that block as Filled. Count up the row/column 8 blocks. Mark that block as Filled. Mark the blocks in between the two (overlap) as Filled.
    # i.e. [8] |--> BOARD row/column: [0,0,0,0,0,0,0,0,0,0] --> [0,0,0,0,0,0,0,1,0,0] --> [0,0,1,0,0,0,0,1,0,0] --> [0,0,1,1,1,1,1,1,0,0]
    # Note: If there are trivial solutions found, we can use this to our advantage:
    # For example: If we have a vert = [[0],...other elem arrs...] and a hort = [[8],...other elem arrs...],
    # Then we can pretend like that row is already filled in, and we can operate on the rows below it as if it were a 9x10 board
    # This can also work if we have a vert = [...other elem arrs...,[0],...other elem arrs...] and a hort = [...other elem arrs...,[8],...other elem arrs...]
    # and change the process respectively
    # i.e. vert contains [0] and hort contains [8] |--> [2,0,0,0,0,0,0,0,0,0] --> [2,0,0,0,0,0,0,0,1,0] --> [2,0,1,0,0,0,0,0,1,0] --> [2,0,1,1,1,1,1,1,1,0]
    # Instead of having just one element in the element array, we could have multiple elements in the element array
    # For example: [1,7] consists of a large element for a 10x10 board because 7 > 10/2, and thus we can do the following operation:
    # Count down the row/column 1 + 1 (space) + 7 blocks. Mark that block as Filled. Count up the row/column 7 blocks. Mark that block as Filled. Mark the blocks in between the two (overlap) as Filled.
    # i.e. [1,7] |--> BOARD row/column: [0,0,0,0,0,0,0,0,0,0] --> [0,0,0,0,0,0,0,0,1,0] --> [0,0,0,1,0,0,0,0,1,0] --> [0,0,0,1,1,1,1,1,1,0]
    # Note: If there are trivial solutions found, we can use this to our advantage:
    # For example: If we have a vert = [[0],...other elem arrs...] and a hort = [[1,7],...other elem arrs...],
    # Then we can pretend like that row is already filled in, and we can operate on the rows below it as if it were a 9x10 board
    # Thus, we get a trivial solution after the first trivial solution was found (row of EMPTY blocks)
    # i.e. [0] in vert and [1,7] in hort |--> [2,0,0,0,0,0,0,0,0,0] --> [2,0,0,0,0,0,0,0,0,1] --> [2,0,0,1,0,0,0,0,0,1] --> [2,1,2,1,1,1,1,1,1,1]
    # The len(hort/vert[elem]) has to be less than or equal 2 because there is too much ambiguity if there are more than 2 elements in the element array
    # For example: [1,4,1] is hard to determine exactly where the possible solutions are without additional information provided by found solutions in the row/column

    # On second thought... maybe we should save the found solutions for another function.
    # This function will just find the possible solutions for each row/column by viewing the large elements (i.e. the elements that are greater than len(board)/2) and return the board with the possible solutions filled in
    
    # First, let us find the possible solutions for each row by viewing the large elements
    # For example: [8] consists of a large element for a 10x10 board because 8 > 10/2, and thus we can do the following operation:
    # Count down the row/column 8 blocks. Mark that block as Filled. Count up the row/column 8 blocks. Mark that block as Filled. Mark the blocks in between the two (overlap) as Filled.
    for i in range(len(hort)):
        if len(hort[i]) == 1 and hort[i][0] > len(board)/2:
            # Count down the row/column hort[i][0] blocks. Mark that block as Filled. Count up the row/column hort[i][0] blocks. Mark that block as Filled. Mark the blocks in between the two (overlap) as Filled.
            board[i][hort[i][0] - 1] = 1
            board[i][len(board) - hort[i][0]] = 1
            for j in range(hort[i][0] - 1, len(board) - hort[i][0],-1):
                board[i][j] = 1
    
    for i in range(len(vert)):
        if len(vert[i]) == 1 and vert[i][0] > len(board)/2:
            # Count down the row/column vert[i][0] blocks. Mark that block as Filled. Count up the row/column vert[i][0] blocks. Mark that block as Filled. Mark the blocks in between the two (overlap) as Filled.
            board[vert[i][0] - 1][i] = 1
            board[len(board) - vert[i][0]][i] = 1
            for j in range(vert[i][0] - 1, len(board) - vert[i][0],-1):
                board[j][i] = 1

    # Next, let us find the possible solutions for each row by viewing pairs of elements
    # For example: [1,7] consists of a large element for a 10x10 board because 7 > 10/2, and thus we can do the following operation:
    # Count down the row/column 1 + 1 (space) + 7 blocks. Mark that block as Filled. Count up the row/column 7 blocks. Mark that block as Filled. Mark the blocks in between the two (overlap) as Filled.
    for i in range(len(hort)):
        if len(hort[i]) == 2 and hort[i][1] + 1 >= len(board) / 2:
            for j in range(len(board) - hort[i][1],sum(hort[i]) + 1):
                board[i][j] = 1
        if len(hort[i]) == 2 and hort[i][0] + 1 >= len(board) / 2:
            for j in range(len(board) - 1 - sum(hort[i]),hort[i][0]):
                board[i][j] = 1
    
    for i in range(len(vert)):
        if len(vert[i]) == 2 and vert[i][1] + 1 >= len(board) / 2:
            for j in range(len(board) - vert[i][1],sum(vert[i]) + 1):
                board[j][i] = 1
        if len(vert[i]) == 2 and vert[i][0] + 1 >= len(board) / 2:
            for j in range(len(board) - 1 - sum(vert[i]),vert[i][0]):
                board[j][i] = 1

    
    return board

# Returns a board that fills in any solved solutions that still have remaining FREE blocks
def check_solved(b, hort, vert):
    board = copy.deepcopy(b)
    # Go through each row and column and check if there are any solved solutions that still have remaining FREE blocks
    # This means I will check to see if there are any FREE blocks that are not marked as Filled or Empty
    # Then I will check to see if in that subgroup, there are any solved solutions
    # e.g. vert has [1,1] at row X and board's row X = [1,0,0,0,0,0,0,0,0,1] -> board changes X to [1,2,2,2,2,2,2,2,2,1]
    # e.g. hort has [7] at col X and board's col X = [0,1,1,1,1,1,1,1,0,0] -> board changes X to [2,1,1,1,1,1,1,1,1,2]

    # First, let us check the columns
    for i in range(len(hort)):
        # If sum(hort[i]) = count of 1's in board[i], then we know that the board[i] is solved
        if sum(hort[i]) == board[i].count(1):
            # Replace all 0 with 2
            for j in range(len(board)):
                if board[i][j] == 0:
                    board[i][j] = 2
    
    # Next, let us check the rows
    for i in range(len(vert)):
        # If sum(vert[i]) = count of 1's in board[i], then we know that the board[i] is solved
        temp = np.transpose(board)
        if sum(vert[i]) == list(temp[i]).count(1):
            # Replace all 0 with 2
            for j in range(len(board)):
                if board[j][i] == 0:
                    board[j][i] = 2
    return board


# Let us define the function that will solve the board
# The function will take in the board, the horizontal array, and the vertical array
# The function will return the solved board
def solve(board, hort, vert):
    while True:
        # First, let us find if there are any trivial solutions (i.e. if a hort/vert element array consists of exactly 0 or exactly len(board) or if the hort/vert element array is adds up to len(board) including the spaces between the blocks [e.g. [0] is trivial, [len(board)] is trivial, [1,13] is trivial for a 15x15 board because there is a sum of 14 + 1 space block = 15, [9,3,1] is trivial for a 15x15 board because there is a sum of 13 + 2 space blocks = 15])
        board = find_trivial(board, hort, vert)
        # Next, let us find the possible solutions for each row/column by viewing the large elements (i.e. the elements that are greater than len(board)/2)
        board = find_large(board, hort, vert)
        if board != check_solved(board, hort, vert):
            return check_solved(board, hort, vert)

    return board

def main():

    # horizontal and vertical arrays
    # hort = [[1], [1, 1], [1, 3], [3, 1], [2]]
    # vert = [[5], [2], [2], [2], [2]]
    hort = [[7], [1, 1, 1], [1, 1, 1], [1, 5], [1], [1], [1, 5], [1, 1, 1], [1, 1, 1], [7]]
    vert = [[0], [2, 2], [1, 1, 1, 1], [1, 1], [1, 1], [4, 4], [1, 1, 1, 1], [1, 4, 1], [1, 1, 1, 1], [3, 3]]
    # hort = [[15],[5,2],[5,2,3,1],[4,2,1,1],[4,2,1],[4,2,1],[2,1,1,1],[1,1,3,1],[1,3,1,2,1],[1,4,1,2,1],[1,4,2],[1,2,1,2],[1,2,3],[2,4],[15]]
    # vert = [[15],[7,2],[6,2,1],[6,4,1],[3,4,1],[1,3,1],[1,2,1,1,1],[1,2,3,2,1],[1,1],[1,2,1],[1,1,1,4,1],[1,1,2,1,2],[1,2,1,1,3],[2,5],[15]]

    # The element's number represents the number of consecutive blocks in the row/column
    # For example: [7] means 7 consecutive blocks in the row/column
    #             [1,1,1] means 1 block, 1 block, 1 block in the row/column
    # When numbers are separated, that means that there is at least one empty space between the blocks


    # Let us define the board based on the provided arrays. Since Mario's Super Picross is always a square, we can just use the length of the horizontal array to define the board
    board = [[0 for x in range(len(hort))] for y in range(len(hort))]
    # The board is a 2D array of 0s, which means that the board is FREE
    # Let us denote our solving annotations as follows:
    # 0 - FREE - blocks or empty spaces that have not been solved yet
    # 1 - BLOCK - blocks that have been solved
    # 2 - EMPTY - empty spaces that have been solved

    # Let us solve the board
    board = solve(board, hort, vert)
    # board = find_trivial(board, hort, vert)
    for row in np.array(board).transpose():
        print(list(row),",")
    show_solution(board)


if __name__ == "__main__":
    main()
