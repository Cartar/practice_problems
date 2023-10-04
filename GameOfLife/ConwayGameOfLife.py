from typing import List
import pdb

def evaluate_NN(cell, N1, N2, N3, N4):
    N_sum = N1 + N2 + N3 + N4
    if N_sum in [0,1,4]:
        return 0
    elif N_sum == 3:
        return 1
    elif N_sum ==2 and cell == 1:
        return 1
    else:
        return 0

def game_of_life(grid: List[List[int]]) -> List[List[int]]:
    """
        Use repeating boundary conditions.

        - If alive with 0,1 or 4 NN then dies
        - If alive with 2,3 NN then lives
        - New life from dead if exactly 3 NN are alive
    """
    N_rows = len(grid)
    N_columns = len(grid[0])

    for r in grid[1:]:
        assert N_columns == len(r), "Ensure all columns have the same length!"

    next_generation = []
    
    for i in range(N_rows):
        next_generation.append([])
        for j in range(N_columns):
            next_r = i + 1
            next_c = j + 1
            if next_r >= N_rows:
                next_r = 0
            if next_c >= N_columns:
                next_c = 0
            #pdb.set_trace()
            next_generation[i].append(
                evaluate_NN(
                    grid[i][j],
                    grid[i-1][j],
                    grid[i][j-1],
                    grid[next_r][j],
                    grid[i][next_c],
                )
            )

    return next_generation

if __name__ == "__main__":

    grid = [
        [0,1,0],
        [0,0,1],
        [1,1,1],
        [0,0,0]
    ]

    print(game_of_life(grid))

    # Returns:
    # [
    #   [0, 0, 0],
    #   [1, 0, 1],
    #   [0, 1, 1],
    #   [0, 1, 0]
    # ]