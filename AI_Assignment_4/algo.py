"""
@author: Patel Parth (2016A7PS0150P)
"""

import my_stats

from collections import deque

from utils import *

def default_heuristic(state):
    var = 0
    while True:
        if state.assignment[var] == 0:
            return var
        var += 1

def MRV_with_degree_heuristic(state, csp, laureate_slots):
    var = default_heuristic(state)
    min_var_lst = [var]
    min_rv = len(laureate_slots[var])
    for next_var in range(var+1, len(state.assignment)):
        if state.assignment[next_var] != 0:
            continue
        if len(laureate_slots[next_var]) == min_rv:
            min_var_lst.append(next_var)
        elif len(laureate_slots[next_var]) < min_rv:
            min_rv = len(laureate_slots[next_var])
            min_var_lst = [next_var]
    if len(min_var_lst) == 1:
        return min_var_lst[0]
    else: # Use degree as tie-breaker
        degree_lst = []
        for next_var in min_var_lst:
            degree = 0
            for neighbor in csp.constraint_graph[next_var]:
                if state.assignment[neighbor] == 0:
                    degree += 1
            degree_lst.append(degree)
        max_idx = 0
        max_degree = degree_lst[0]
        for idx in range(1, len(degree_lst)):
            if degree_lst[idx] > max_degree:
                max_degree = degree_lst[idx]
                max_idx = idx
        return min_var_lst[max_idx]

def forward_checking(next_var, value, csp, laureate_slots):
    next_laureate_slots = []
    for slots in laureate_slots:
        next_laureate_slots.append(set(slots))
    for neighbor in csp.constraint_graph[next_var]:
        next_laureate_slots[neighbor].discard(value)
    return next_laureate_slots

def dfs_backtracking(csp, heuristic, initial_state, variable_order):
    # initial_state = State(csp.no_of_laureates)
    # variable_order = []
    laureate_slots = []
    for lst in csp.laureates_lst:
        laureate_slots.append(set(lst))
    return recursive_backtracking(initial_state, csp, laureate_slots, heuristic, variable_order, 1)

def recursive_backtracking(state, csp, laureate_slots, heuristic, variable_order, depth):
    if my_stats.MAX_DEPTH < depth:
        my_stats.MAX_DEPTH = depth
    if state.is_assignment_complete():
        return state
    if heuristic == 'default':
        next_var = default_heuristic(state)
    elif heuristic == 'MRV_with_degree':
        next_var = MRV_with_degree_heuristic(state, csp, laureate_slots)
    variable_order.append(next_var)
    for value in laureate_slots[next_var]:
        if check_consistency(csp, state, next_var, value):
            state.assign_value(next_var, value)
            if my_stats.NO_OF_NODES % 100 == 0:
                my_stats.assignment_seq.append(list(state.assignment))
                my_stats.variable_seq.append(list(variable_order))
            my_stats.NO_OF_NODES += 1
            if heuristic == 'default':
                state = recursive_backtracking(state, csp, laureate_slots, heuristic, variable_order, depth+1)
            elif heuristic == 'MRV_with_degree':
                next_laureate_slots = forward_checking(next_var, value, csp, laureate_slots)
                state = recursive_backtracking(state, csp, next_laureate_slots, heuristic, variable_order, depth+1)
                del next_laureate_slots
            if state.is_assignment_complete():
                return state
            state.unassign_value(next_var)
    variable_order.pop()
    return state
    
def AC3(csp):
    queue = deque()
    for l1, nbd_set in enumerate(csp.constraint_graph):
        for l2 in nbd_set:
            queue.append((l1, l2))
    while len(queue) > 0:
        l1, l2 = queue.popleft()
        if remove_inconsistent_values(l1, l2, csp):
            for neighbor in csp.constraint_graph[l1]:
                if neighbor == l2:
                    continue
                queue.append((neighbor, l1))
    return csp

def remove_inconsistent_values(l1, l2, csp):
    removed = False
    removed_vals = []
    for x in csp.laureates_lst[l1]:
        flag = False
        for y in csp.laureates_lst[l2]:
            if x != y:
                flag = True
                break
        if flag == False:
            removed_vals.append(x)
            removed = True
    for val in removed_vals:
        csp.laureates_lst[l1].discard(val)
    return removed
