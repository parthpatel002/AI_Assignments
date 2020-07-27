"""
@author: Patel Parth (2016A7PS0150P)
"""

"""
Notations for board state:
0 means empty cell
1 means green coin (Machine M) on cell
2 means blue coin (Human H) on cell
"""

TOTAL_NODES = 0

# State Representation for Min-Max and Alpha-Beta Pruning Algorithm
class State:
    def __init__(self, N, board = None):
        self.N = N
        if board == None:
            self.board = bytearray(N*N)
        else:
            self.board = board
        self.game_over = False
        self.game_util_val = 0
    def place_coin(self, x, y, coin):
        """ coin - 1 for machine, 2 for human """
        self.board[x*self.N+y] = coin
    def is_game_over(self):
        """ Returns either (False, _) or (True, utility_value) """
        n = self.N
        for i in range(n):
            for j in range(n-2):
                if self.board[i*n+j]==1 and self.board[i*n+j+1]==1 and self.board[i*n+j+2]==1:
                    self.game_over = True
                    self.game_util_val = 1
                    return (True, 1)
                elif self.board[i*n+j]==2 and self.board[i*n+j+1]==2 and self.board[i*n+j+2]==2:
                    self.game_over = True
                    self.game_util_val = -1
                    return (True, -1)
        for j in range(n):
            for i in range(n-2):
                if self.board[i*n+j]==1 and self.board[(i+1)*n+j]==1 and self.board[(i+2)*n+j]==1:
                    self.game_over = True
                    self.game_util_val = 1
                    return (True, 1)
                elif self.board[i*n+j]==2 and self.board[(i+1)*n+j]==2 and self.board[(i+2)*n+j]==2:
                    self.game_over = True
                    self.game_util_val = -1
                    return (True, -1)
        for i in range(n-2):
            for j in range(n-2):
                if self.board[i*n+j]==1 and self.board[(i+1)*n+j+1]==1 and self.board[(i+2)*n+j+2]==1:
                    self.game_over = True
                    self.game_util_val = 1
                    return (True, 1)
                elif self.board[i*n+j]==2 and self.board[(i+1)*n+j+1]==2 and self.board[(i+2)*n+j+2]==2:
                    self.game_over = True
                    self.game_util_val = -1
                    return (True, -1)
        for i in range(n-2):
            for j in range(2, n):
                if self.board[i*n+j]==1 and self.board[(i+1)*n+j-1]==1 and self.board[(i+2)*n+j-2]==1:
                    self.game_over = True
                    self.game_util_val = 1
                    return (True, 1)
                elif self.board[i*n+j]==2 and self.board[(i+1)*n+j-1]==2 and self.board[(i+2)*n+j-2]==2:
                    self.game_over = True
                    self.game_util_val = -1
                    return (True, -1)
        for j in range(n):
            if self.board[(n-1)*n+j] == 0:
                return (False, 0)
        self.game_over = True
        self.game_util_val = 0
        return (True, 0)

def return_next_possible_actions(state):
    """
    Returns list of (col_no, row_no), where each (col_no, row_no) denotes a possible action
    """
    action_lst = []
    n = state.N
    for j in range(n):
        idx = 0
        while idx < n and state.board[idx*n+j] != 0:
            idx += 1
        if idx < n:
            action_lst.append((j, idx))
    # action_lst.sort(key = lambda x: -1*x[1])
    return action_lst

def create_next_state(state, action, coin):
    """
    Create next state; action is (col_no, row_no); coin - 1 for machine, 2 for human;
    """
    global TOTAL_NODES
    TOTAL_NODES += 1
    # if TOTAL_NODES % 1000 == 0:
    # print(TOTAL_NODES)
    nxt_state = State(state.N, board=bytearray(state.board))
    nxt_state.place_coin(action[1], action[0], coin)
    return nxt_state
