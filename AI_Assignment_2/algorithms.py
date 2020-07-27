"""
@author: Patel Parth (2016A7PS0150P)
"""

from utils import *
import heapq
import math

# Hill Climbing Algo.
def hill_climbing(prev_state, heuristic_fn):
    """
    Returns the move that will fetch next_state from prev_state based on heuristic_fn and hill_climbing
    Solves a Minimization Problem
    """
    N = prev_state.N
    for i in range(N):
        for j in range(N):
            if prev_state.curr_board[i*N+j] == 10 and heuristic_fn(prev_state, i, j) == 1:
                prev_state.curr_board[i*N+j] = 9 # Flag the definite mines
    coords_list = []
    h_val_list = []
    for i in range(N):
        for j in range(N):
            if prev_state.curr_board[i*N+j] == 10:
                coords_list.append((i, j))
                h_val_list.append(heuristic_fn(prev_state, i, j))
    # if h_val_list == []:
    #     return None
    min_idx = 0
    for idx in range(1, len(h_val_list)):
        if h_val_list[idx] < h_val_list[min_idx]:
            min_idx = idx
    # if h_val_list[min_idx] == 1:
    #     return None
    return coords_list[min_idx]

# Stochastic Hill Climbing Algo.
def stochastic_hill_climbing(prev_state, heuristic_fn):
    """
    Returns the move that will fetch next_state from prev_state based on heuristic_fn and stochastic_hill_climbing
    Solves a Minimization Problem
    """
    N = prev_state.N
    for i in range(N):
        for j in range(N):
            if prev_state.curr_board[i*N+j] == 10 and heuristic_fn(prev_state, i, j) == 1:
                prev_state.curr_board[i*N+j] = 9 # Flag the definite mines
    coords_list = []
    h_val_list = []
    for i in range(N):
        for j in range(N):
            if prev_state.curr_board[i*N+j] == 10:
                coords_list.append((i, j))
                h_val_list.append(heuristic_fn(prev_state, i, j))
    # if h_val_list == []:
    #     return None
    sum_h_val = 0
    for h_val in h_val_list:
        sum_h_val += (1-h_val)
    cumulative_h_val_list = []
    cumulative_h_val_list.append((1-h_val_list[0])/sum_h_val)
    for idx in range(1, len(h_val_list)):
        cumulative_h_val_list.append(cumulative_h_val_list[-1]+(1-h_val_list[idx])/sum_h_val)
    rand_choice = random.random()
    for idx in range(len(cumulative_h_val_list)):
        if rand_choice <= cumulative_h_val_list[idx]:
            break
    return coords_list[idx]

# Local Beam Search Algo.
def local_beam_search(prev_states, heuristic_fn, K):
    """
    Returns moves to generate k best next_states from  a list prev_states of length k based on heuristic_fn
    Solves a Minimization Problem
    """
    N = prev_states[0].N
    for prev_state in prev_states:
        for i in range(N):
            for j in range(N):
                if prev_state.curr_board[i*N+j] == 10 and heuristic_fn(prev_state, i, j) == 1:
                    prev_state.curr_board[i*N+j] = 9 # Flag the definite mines
    coords_list = []
    h_val_list = []
    for idx in range(len(prev_states)):
        prev_state = prev_states[idx]
        for i in range(N):
            for j in range(N):
                if prev_state.curr_board[i*N+j] == 10:
                    coords_list.append((idx, i, j))
                    h_val_list.append(heuristic_fn(prev_state, i, j))
    K_min_indices = heapq.nsmallest(K, range(len(h_val_list)), h_val_list.__getitem__)
    moves_list = []
    for idx in K_min_indices:
        moves_list.append(coords_list[idx])
    return moves_list

# Simulated Annealing Algo.
def simulated_annealing(prev_state, heuristic_fn, T, threshold):
    """
    Returns the move that will fetch next_state from prev_state based on heuristic_fn and simulated_annealing
    Solves a Minimization Problem
    """
    global SA_nbd_threshold_idx, SA_nbd_threshold_list
    N = prev_state.N
    for i in range(N):
        for j in range(N):
            if prev_state.curr_board[i*N+j] == 10 and heuristic_fn(prev_state, i, j) == 1:
                prev_state.curr_board[i*N+j] = 9 # Flag the definite mines
    available_moves_coords = []
    for i in range(N):
        for j in range(N):
            if prev_state.curr_board[i*N+j] == 10 and prev_state.is_adjacent_to_open_square(i, j) >= SA_nbd_threshold_list[SA_nbd_threshold_idx]:
                available_moves_coords.append((i, j))
    if available_moves_coords == []:
        SA_nbd_threshold_idx = (SA_nbd_threshold_idx+1)%len(SA_nbd_threshold_list)
        return None
    x_chosen, y_chosen = random.choice(available_moves_coords)
    h_val_chosen = heuristic_fn(prev_state, x_chosen, y_chosen)
    if h_val_chosen <= threshold:
        # print("Positive deltaE chosen")
        return (x_chosen, y_chosen)
    else:
        deltaE = threshold - h_val_chosen
        probability = math.exp(deltaE/T)
        if random.random() < probability:
            # print("Negative deltaE chosen")
            return (x_chosen, y_chosen)
        else:
            return None

SA_nbd_threshold_list = [0.375, 0.375, 0.375, 0.250, 0.250, 0.125, 0.50]
SA_nbd_threshold_idx = 0

