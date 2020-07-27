"""
@author: Patel Parth (2016A7PS0150P)
"""

import random
from collections import deque

"""
Notations for board state:
0 means empty cell and not adjacent to any mine
1-8 means empty cell and adjacent to 1-8 mines
9 means a mine in the orig_board
9 also means a mine that has been detected/flagged in curr_board by the algorithm
10 means an unexplored mine in curr_board
11 means a mine which is stepped upon in curr_board - denoting a local optima
"""

# State Representation for Optimization Problem
class State:
    def __init__(self, N, M, board):
        self.N = N # NxN board
        self.M = M # Number of mines
        self.orig_board = board # Actual state of board
        self.curr_board = bytearray(N*N) # Current state of board
        for idx in range(N*N):
            self.curr_board[idx] = 10 # 10 means unexplored square
        self.game_over = False # Indicates if we can play further or not
        self.game_lost = False # Indicates if we have lost the game or not
    def is_goal_state(self):
        """Check if we have won the game i.e. reached the global optima"""
        for idx in range(self.N*self.N):
            if self.orig_board[idx] == 9:
                continue
            if self.orig_board[idx] != self.curr_board[idx]:
                return False
        self.game_over = True
        self.game_lost = False
        return True
    def is_mine(self, x, y):
        if self.orig_board[x*self.N+y] == 9:
            return True
        return False
    def is_adjacent_to_mine(self, x, y):
        if self.orig_board[x*self.N+y] > 0 and self.orig_board[x*self.N+y] < 9:
            return True
        return False
    def stepped_on_mine(self, x, y):
        self.curr_board[x*self.N+y] = 11 # 11 means stepped on that mine
        self.game_over = True
        self.game_lost = True
    def is_adjacent_to_open_square(self, x, y):
        x_coords = [-1,-1,-1,0,0,1,1,1]
        y_coords = [-1,0,1,-1,1,-1,0,1]
        Nr = 0
        Dr = 0
        for i, j in zip(x_coords, y_coords):
            if (x+i < self.N) and (x+i >= 0) and (y+j < self.N) and (y+j >= 0):
                Dr += 1
                if self.curr_board[(x+i)*self.N+(y+j)] != 10:
                    Nr += 1
        return Nr/Dr
    def get_branching_factor(self):
        b_f = 0
        for i in range(self.N):
            for j in range(self.N):
                if self.curr_board[i*self.N+j] == 10:
                    b_f += 1
        return b_f
    def open_on_click(self, x, y):
        """
        Open the adjacent area on clicking at (x,y)
        Assumption is that self.orig_board[x*self.N+y]==0,1,2,3,4,5,6,7,8 and self.curr_board[x*self.N+y]==10
        """
        self.curr_board[x*self.N+y] = self.orig_board[x*self.N+y]
        if x == 0:
            up_idx = 0
        else:
            up_idx = 1
            while True:
                if x-up_idx == 0:
                    break
                if self.orig_board[(x-up_idx)*self.N+y] == 9 or self.curr_board[(x-up_idx)*self.N+y] != 10:
                    up_idx -= 1
                    break
                if (y-1 >= 0 and self.orig_board[(x-up_idx)*self.N+(y-1)] == 9) or (y+1 < self.N and self.orig_board[(x-up_idx)*self.N+(y+1)] == 9):
                    break
                up_idx += 1
        if x == self.N-1:
            down_idx = 0
        else:
            down_idx = 1
            while True:
                if x+down_idx == self.N-1:
                    break
                if self.orig_board[(x+down_idx)*self.N+y] == 9 or self.curr_board[(x+down_idx)*self.N+y] != 10:
                    down_idx -= 1
                    break
                if (y-1 >= 0 and self.orig_board[(x+down_idx)*self.N+(y-1)] == 9) or (y+1 < self.N and self.orig_board[(x+down_idx)*self.N+(y+1)] == 9):
                    break
                down_idx += 1
        if y == 0:
            left_idx = 0
        else:
            left_idx = 1
            while True:
                if y-left_idx == 0:
                    break
                if self.orig_board[x*self.N+(y-left_idx)] == 9 or self.curr_board[x*self.N+(y-left_idx)] != 10:
                    left_idx -= 1
                    break
                if (x-1 >= 0 and self.orig_board[(x-1)*self.N+(y-left_idx)] == 9) or (x+1 < self.N and self.orig_board[(x+1)*self.N+(y-left_idx)] == 9):
                    break
                left_idx += 1
        if y == self.N-1:
            right_idx = 0
        else:
            right_idx = 1
            while True:
                if y+right_idx == self.N-1:
                    break
                if self.orig_board[x*self.N+(y+right_idx)] == 9 or self.curr_board[x*self.N+(y+right_idx)] != 10:
                    right_idx -= 1
                    break
                if (x-1 >= 0 and self.orig_board[(x-1)*self.N+(y+right_idx)] == 9) or (x+1 < self.N and self.orig_board[(x+1)*self.N+(y+right_idx)] == 9):
                    break
                right_idx += 1
        for idx in range(1,up_idx+1):
            self.curr_board[(x-idx)*self.N+y] = self.orig_board[(x-idx)*self.N+y]
        for idx in range(1,down_idx+1):
            self.curr_board[(x+idx)*self.N+y] = self.orig_board[(x+idx)*self.N+y]
        for idx in range(1,left_idx+1):
            self.curr_board[(x)*self.N+(y-idx)] = self.orig_board[(x)*self.N+(y-idx)]
        for idx in range(1,right_idx+1):
            self.curr_board[(x)*self.N+(y+idx)] = self.orig_board[(x)*self.N+(y+idx)]
        max_idx = up_idx
        for j in range(1, left_idx+1):
            y_eff = y-j
            for idx in range(1, max_idx+1):
                if self.orig_board[(x-idx)*self.N+y_eff] == 9 or self.curr_board[(x-idx)*self.N+y_eff] != 10:
                    max_idx = idx-1
                    break
                self.curr_board[(x-idx)*self.N+y_eff] = self.orig_board[(x-idx)*self.N+y_eff]
        max_idx = down_idx
        for j in range(1, left_idx+1):
            y_eff = y-j
            for idx in range(1, max_idx+1):
                if self.orig_board[(x+idx)*self.N+y_eff] == 9 or self.curr_board[(x+idx)*self.N+y_eff] != 10:
                    max_idx = idx-1
                    break
                self.curr_board[(x+idx)*self.N+y_eff] = self.orig_board[(x+idx)*self.N+y_eff]
        max_idx = up_idx
        for j in range(1, right_idx+1):
            y_eff = y+j
            for idx in range(1, max_idx+1):
                if self.orig_board[(x-idx)*self.N+y_eff] == 9 or self.curr_board[(x-idx)*self.N+y_eff] != 10:
                    max_idx = idx-1
                    break
                self.curr_board[(x-idx)*self.N+y_eff] = self.orig_board[(x-idx)*self.N+y_eff]
        max_idx = down_idx
        for j in range(1, right_idx+1):
            y_eff = y+j
            for idx in range(1, max_idx+1):
                if self.orig_board[(x+idx)*self.N+y_eff] == 9 or self.curr_board[(x+idx)*self.N+y_eff] != 10:
                    max_idx = idx-1
                    break
                self.curr_board[(x+idx)*self.N+y_eff] = self.orig_board[(x+idx)*self.N+y_eff]
        # x_coords = [-1,-1,-1,0,0,1,1,1]
        # y_coords = [-1,0,1,-1,1,-1,0,1]
        # q = deque()
        # visited = set()
        # q.append((x, y))
        # visited.add((x, y))
        # while len(q) > 0:
        #     x1, y1 = q.popleft()
        #     self.curr_board[x1*self.N+y1] = self.orig_board[x1*self.N+y1]
        #     if self.orig_board[x1*self.N+y1]==0:
        #         for i, j in zip(x_coords, y_coords):
        #             if (x1+i < self.N) and (x1+i >= 0) and (y1+j < self.N) and (y1+j >= 0) and ((x1+i, y1+j) not in visited) and self.curr_board[(x1+i)*self.N+(y1+j)]==10:
        #                 q.append((x1+i, y1+j))
        #                 visited.add((x1+i, y1+j))
        

def mine_generator(N, M):
    """
    Generate M mines randomly on a N*N board
    """
    board = bytearray(N*N)
    mines = random.sample(range(N*N), M)
    for mine in mines:
        board[mine] = 9 # 9 means presence of mine
    x_coords = [-1,-1,-1,0,0,1,1,1]
    y_coords = [-1,0,1,-1,1,-1,0,1]
    for i in range(N):
        for j in range(N):
            if board[i*N+j] == 9:
                continue
            cnt = 0
            for x, y in zip(x_coords, y_coords):
                if i+x < N and i+x >= 0 and j+y < N and j+y >= 0 and board[(i+x)*N+(j+y)] == 9:
                    cnt += 1
            board[i*N+j] = cnt
    return State(N, M, board)

def first_click(state):
    """
    Take the first step by clicking blindly on any square
    """
    while True:
        x = random.randrange(0, state.N, 1) # First click's x-coordinate between 0 and N-1
        y = random.randrange(0, state.N, 1) # First click's y-coordinate between 0 and N-1
        if state.is_mine(x, y):
            if random.random() < 0.1:
                state.stepped_on_mine(x, y)
                return state, x, y
        elif not state.is_adjacent_to_mine(x, y):
            state.open_on_click(x, y)
            return state, x, y

def next_state(state, x, y):
    """
    Generates next state obtained by clicking on (x,y) in state
    """
    if state.is_mine(x, y):
        state.stepped_on_mine(x, y)
    else:
        state.open_on_click(x, y)
    return state

def duplicate_state(state):
    state_v2 = State(state.N, state.M, state.orig_board)
    state_v2.game_over = state.game_over
    state_v2.game_lost = state.game_lost
    state_v2.curr_board = bytearray(state.curr_board)
    return state_v2

def next_state_v2(state, x, y):
    """
    Generate next state by clicking on (x,y)
    """
    state_v2 = duplicate_state(state)
    if state_v2.is_mine(x, y):
        state_v2.stepped_on_mine(x, y)
    else:
        state_v2.open_on_click(x, y)
    return state_v2
