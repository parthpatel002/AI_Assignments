"""
@author: Patel Parth (2016A7PS0150P)
"""

from utils import *

MAX_DEPTH = 6

def heuristic(state, mode):
    """
    Estimate outcome/utility-value of a non-terminal state
    mode - 1 for MAX node i.e. its Machine's turn to make a move; 2 for MIN node i.e. its Human's turn to make a move.
    """
    action_lst = return_next_possible_actions(state)
    action_set = set()
    for action in action_lst:
        action_set.add((action[1], action[0]))
    M_wins = 0
    H_wins = 0
    n = state.N
    for i in range(n):
        for j in range(n-2):
            if (state.board[i*n+j]==1 and state.board[i*n+j+1]==1 and (i, j+2) in action_set):
                M_wins += 1
            elif (state.board[i*n+j]==1 and (i, j+1) in action_set and state.board[i*n+j+2]==1):
                M_wins += 1
            elif ((i, j) in action_set and state.board[i*n+j+1]==1 and state.board[i*n+j+2]==1):
                M_wins += 1
            if (state.board[i*n+j]==2 and state.board[i*n+j+1]==2 and (i, j+2) in action_set):
                H_wins += 1
            elif (state.board[i*n+j]==2 and (i, j+1) in action_set and state.board[i*n+j+2]==2):
                H_wins += 1
            elif ((i, j) in action_set and state.board[i*n+j+1]==2 and state.board[i*n+j+2]==2):
                H_wins += 1
    for j in range(n):
        for i in range(n-2):
            if (state.board[i*n+j]==1 and state.board[(i+1)*n+j]==1 and (i+2, j) in action_set):
                M_wins += 1
            elif (state.board[i*n+j]==1 and (i+1, j) in action_set and state.board[(i+2)*n+j]==1):
                M_wins += 1
            elif ((i, j) in action_set and state.board[(i+1)*n+j]==1 and state.board[(i+2)*n+j]==1):
                M_wins += 1
            if (state.board[i*n+j]==2 and state.board[(i+1)*n+j]==2 and (i+2, j) in action_set):
                H_wins += 1
            elif (state.board[i*n+j]==2 and (i+1, j) in action_set and state.board[(i+2)*n+j]==2):
                H_wins += 1
            elif ((i, j) in action_set and state.board[(i+1)*n+j]==2 and state.board[(i+2)*n+j]==2):
                H_wins += 1
    for i in range(n-2):
        for j in range(n-2):
            if (state.board[i*n+j]==1 and state.board[(i+1)*n+j+1]==1 and (i+2, j+2) in action_set):
                M_wins += 1
            elif (state.board[i*n+j]==1 and (i+1, j+1) in action_set and state.board[(i+2)*n+j+2]==1):
                M_wins += 1
            elif ((i, j) in action_set and state.board[(i+1)*n+j+1]==1 and state.board[(i+2)*n+j+2]==1):
                M_wins += 1
            if (state.board[i*n+j]==2 and state.board[(i+1)*n+j+1]==2 and (i+2, j+2) in action_set):
                H_wins += 1
            elif (state.board[i*n+j]==2 and (i+1, j+1) in action_set and state.board[(i+2)*n+j+2]==2):
                H_wins += 1
            elif ((i, j) in action_set and state.board[(i+1)*n+j+1]==2 and state.board[(i+2)*n+j+2]==2):
                H_wins += 1
    for i in range(n-2):
        for j in range(2, n):
            if (state.board[i*n+j]==1 and state.board[(i+1)*n+j-1]==1 and (i+2, j-2) in action_set):
                M_wins += 1           
            elif (state.board[i*n+j]==1 and (i+1, j-1) in action_set and state.board[(i+2)*n+j-2]==1):
                M_wins += 1
            elif ((i, j) in action_set and state.board[(i+1)*n+j-1]==1 and state.board[(i+2)*n+j-2]==1):
                M_wins += 1
            if (state.board[i*n+j]==2 and state.board[(i+1)*n+j-1]==2 and (i+2, j-2) in action_set):
                H_wins += 1           
            elif (state.board[i*n+j]==2 and (i+1, j-1) in action_set and state.board[(i+2)*n+j-2]==2):
                H_wins += 1
            elif ((i, j) in action_set and state.board[(i+1)*n+j-1]==2 and state.board[(i+2)*n+j-2]==2):
                H_wins += 1
    if mode == 1:
        if M_wins >= 1:
            return 1
        elif H_wins >= 2:
            return -1
        else:
            return 0
    elif mode == 2:
        if H_wins >= 1:
            return -1
        elif M_wins >= 2:
            return 1
        else:
            return 0  

def minimax_decision(state):
    """
    Returns action [i.e.(col_no, row_no)] to reach next state
    """
    _, action = max_value(state, 0)
    return action

def max_value(state, depth):
    """
    Returns (utility value, action) corresponding to MAX node
    """
    global MAX_DEPTH
    cond, val = state.is_game_over()
    if cond:
        return (val, None)
    if depth == MAX_DEPTH:
        # print("Hello")
        return (heuristic(state, 1), None)
    max_val = -2
    max_action = None
    action_lst = return_next_possible_actions(state)
    for action in action_lst:
        nxt_state = create_next_state(state, action, 1) # as MAX node corresponds to move by Machine M
        nxt_val, _ = min_value(nxt_state, depth+1)
        if nxt_val > max_val:
            max_val = nxt_val
            max_action = action
        del nxt_state
    return (max_val, max_action)

def min_value(state, depth):
    """
    Returns (utility value, action) corresponding to MIN node
    """
    global MAX_DEPTH
    cond, val = state.is_game_over()
    if cond:
        return (val, None)
    if depth == MAX_DEPTH:
        # print("Hello")
        return (heuristic(state, 2), None)
    min_val = 2
    min_action = None
    action_lst = return_next_possible_actions(state)
    for action in action_lst:
        nxt_state = create_next_state(state, action, 2) # as MIN node corresponds to move by Human H
        nxt_val, _ = max_value(nxt_state, depth+1)
        if nxt_val < min_val:
            min_val = nxt_val
            min_action = action 
        del nxt_state
    return (min_val, min_action)

def alpha_beta_pruning_decision(state):
    """
    Returns action [i.e.(col_no, row_no)] to reach next state
    """
    _, action = max_value_alpha_beta(state, 0, -2, 2)
    return action

def max_value_alpha_beta(state, depth, alpha, beta):
    """
    Returns (utility value, action) corresponding to MAX node
    """
    global MAX_DEPTH
    cond, val = state.is_game_over()
    if cond:
        return (val, None)
    if depth == MAX_DEPTH:
        # print("Hello")
        return (heuristic(state, 1), None)
    max_val = -2
    max_action = None
    action_lst = return_next_possible_actions(state)
    for action in action_lst:
        nxt_state = create_next_state(state, action, 1) # as MAX node corresponds to move by Machine M
        nxt_val, _ = min_value_alpha_beta(nxt_state, depth+1, alpha, beta)
        if nxt_val > max_val:
            max_val = nxt_val
            max_action = action
        if max_val >= beta:
            return (max_val, max_action)
        if alpha < max_val:
            alpha = max_val
        del nxt_state
    return (max_val, max_action)

def min_value_alpha_beta(state, depth, alpha, beta):
    """
    Returns (utility value, action) corresponding to MIN node
    """
    global MAX_DEPTH
    cond, val = state.is_game_over()
    if cond:
        return (val, None)
    if depth == MAX_DEPTH:
        # print("Hello")
        return (heuristic(state, 2), None)
    min_val = 2
    min_action = None
    action_lst = return_next_possible_actions(state)
    for action in action_lst:
        nxt_state = create_next_state(state, action, 2) # as MIN node corresponds to move by Human H
        nxt_val, _ = max_value_alpha_beta(nxt_state, depth+1, alpha, beta)
        if min_val > nxt_val:
            min_val = nxt_val
            min_action = action 
        if min_val <= alpha:
            return (min_val, min_action)
        if beta > min_val:
            beta = min_val
        del nxt_state
    return (min_val, min_action)
