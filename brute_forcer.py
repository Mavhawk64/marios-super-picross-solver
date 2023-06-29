from itertools import product


def solve_picross(x_axis, y_axis, partial_grid=None):
    row_length = len(y_axis)
    col_length = len(x_axis)
    solution = partial_grid if partial_grid is not None else [
        [0] * col_length for _ in range(row_length)]

    def is_valid():
        # Check row constraints
        for i in range(row_length):
            row = solution[i]
            blocks = get_blocks(row)
            if blocks != y_axis[i]:
                return False

        # Check column constraints
        for j in range(col_length):
            col = [solution[i][j] for i in range(row_length)]
            blocks = get_blocks(col)
            if blocks != x_axis[j]:
                return False

        return True

    def get_blocks(lst):
        blocks = []
        count = 0
        for num in lst:
            if num == 1:
                count += 1
            elif count > 0:
                blocks.append(count)
                count = 0
        if count > 0:
            blocks.append(count)
        return blocks

    ambiguous_indices = [(i, j) for i in range(row_length)
                         for j in range(col_length) if partial_grid[i][j] == 0]

    for configuration in product([1, 2], repeat=len(ambiguous_indices)):
        for idx, value in enumerate(configuration):
            i, j = ambiguous_indices[idx]
            solution[i][j] = value

        if is_valid():
            return solution

    return None


x_axis = [[7], [1, 1, 1], [1, 1, 1], [1, 5], [
    1], [1], [1, 5], [1, 1, 1], [1, 1, 1], [7]]
y_axis = [[0], [2, 2], [1, 1, 1, 1], [1, 1], [1, 1], [
    4, 4], [1, 1, 1, 1], [1, 4, 1], [1, 1, 1, 1], [3, 3]]
partial_grid = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 2, 1, 1, 1, 1],
    [1, 2, 2, 1, 2, 2, 1, 2, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

solution = solve_picross(x_axis, y_axis, partial_grid)

if solution is not None:
    for row in solution:
        print(row)
else:
    print("No solution found.")
