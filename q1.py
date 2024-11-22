import random

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def print_puzzle(state):
    for row in state:
        print(row)
    print()

def is_goal_state(state):
    return state == goal_state

def get_blank_position(state):
    for row in range(3):
        for col in range(3):
            if state[row][col] == 0:
                return row, col
    return None

def valid_moves(blank_pos):
    row, col = blank_pos
    moves = []
    if row > 0: moves.append((-1, 0))
    if row < 2: moves.append((1, 0))
    if col > 0: moves.append((0, -1))
    if col < 2: moves.append((0, 1))
    return moves

def apply_move(state, blank_pos, move):
    row, col = blank_pos
    new_row, new_col = row + move[0], col + move[1]
    new_state = [row[:] for row in state]
    new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
    return new_state

def manhattan_distance(state):
    distance = 0
    for r in range(3):
        for c in range(3):
            tile = state[r][c]
            if tile != 0:
                goal_r, goal_c = divmod(tile - 1, 3)
                distance += abs(goal_r - r) + abs(goal_c - c)
    return distance

def misplaced_tiles(state):
    count = 0
    for r in range(3):
        for c in range(3):
            if state[r][c] != 0 and state[r][c] != goal_state[r][c]:
                count += 1
    return count

def hill_climbing(initial_state, heuristic_fn):
    current_state = initial_state
    path = [current_state]
    
    while not is_goal_state(current_state):
        blank_pos = get_blank_position(current_state)
        neighbors = []
        for move in valid_moves(blank_pos):
            neighbor = apply_move(current_state, blank_pos, move)
            neighbors.append(neighbor)
        
        neighbor_scores = [(neighbor, heuristic_fn(neighbor)) for neighbor in neighbors]
        neighbor_scores.sort(key=lambda x: x[1])
        
        if len(neighbor_scores) == 0 or neighbor_scores[0][1] >= heuristic_fn(current_state):
            print("No improvement, stuck at local maxima/plateau.")
            break
        
        current_state = neighbor_scores[0][0]
        path.append(current_state)
    
    return path

if __name__ == "__main__":
    initial_state = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]

    print("Initial State:")
    print_puzzle(initial_state)

    path = hill_climbing(initial_state, manhattan_distance)

    print("\nPath to goal:")
    for state in path:
        print_puzzle(state)

    initial_state_2 = [[2, 1, 3], [4, 5, 6], [7, 8, 0]]
    print("Testing with a different initial state:")
    print_puzzle(initial_state_2)
    path_2 = hill_climbing(initial_state_2, manhattan_distance)
    print("\nPath to goal:")
    for state in path_2:
        print_puzzle(state)
