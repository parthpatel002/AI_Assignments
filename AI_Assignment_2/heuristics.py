"""
@author: Patel Parth (2016A7PS0150P)
"""

from utils import *

def observe_nbd_cell(prev_state, x1, y1):
    """
    Assumption is that prev_state.curr_board[x1*N+y1] is 1-8
    """
    N = prev_state.N
    nbd_mine_cnt = prev_state.curr_board[x1*N+y1]
    possible_nbd_mine_cnt = 0
    actual_nbd_mine_cnt = 0
    x_coords = [-1,-1,-1,0,0,1,1,1]
    y_coords = [-1,0,1,-1,1,-1,0,1]
    for i, j in zip(x_coords, y_coords):
        if i+x1 < N and i+x1 >= 0 and j+y1 < N and j+y1 >= 0:
            if prev_state.curr_board[(i+x1)*N+(j+y1)] == 9:
                actual_nbd_mine_cnt += 1
            elif prev_state.curr_board[(i+x1)*N+(j+y1)] == 10:
                possible_nbd_mine_cnt += 1
    return (nbd_mine_cnt-actual_nbd_mine_cnt)/possible_nbd_mine_cnt

def heuristic1(prev_state, x, y):
    """
    Returns heuristic value of state obtained by clicking at (x,y) on prev_state's board
    Assumption is that prev_state.curr_board[x*N+y] is 10
    Returns value between 0 and 1
    """
    N = prev_state.N
    nbd_val_list = []
    x_coords = [-1,-1,-1,0,0,1,1,1]
    y_coords = [-1,0,1,-1,1,-1,0,1]
    for i, j in zip(x_coords, y_coords):
        if i+x < N and i+x >= 0 and j+y < N and j+y >= 0:
            if prev_state.curr_board[(i+x)*N+(j+y)] == 9 or prev_state.curr_board[(i+x)*N+(j+y)] == 10:
                nbd_val_list.append(0.5)
            else:
                nbd_val_list.append(observe_nbd_cell(prev_state, i+x, j+y))
    if 1 in nbd_val_list:
        return 1
    elif 0 in nbd_val_list:
        return 0
    else:
        max_val = 0 # We choose maximum as we wish to avoid an uncertain move i.e. we prefer a move whose maximum will be minimum.
        for val in nbd_val_list:
            if val > max_val:
                max_val = val
        return max_val

def heuristic2(prev_state, x, y):
    """
    Returns heuristic value of state obtained by clicking at (x,y) on prev_state's board
    Assumption is that prev_state.curr_board[x*N+y] is 10
    Returns value between 0 and 1
    """
    N = prev_state.N
    nbd_val_list = []
    x_coords = [-1,-1,-1,0,0,1,1,1]
    y_coords = [-1,0,1,-1,1,-1,0,1]
    for i, j in zip(x_coords, y_coords):
        if i+x < N and i+x >= 0 and j+y < N and j+y >= 0:
            if prev_state.curr_board[(i+x)*N+(j+y)] == 9 or prev_state.curr_board[(i+x)*N+(j+y)] == 10:
                nbd_val_list.append(0.5)
            else:
                nbd_val_list.append(observe_nbd_cell(prev_state, i+x, j+y))
    if 1 in nbd_val_list:
        return 1
    elif 0 in nbd_val_list:
        return 0
    else:
        sum = 0
        for val in nbd_val_list:
            sum += val
        return sum/len(nbd_val_list)
