"""
@author: Patel Parth (2016A7PS0150P)
"""

# GROUP_FILE = "group_data.txt"
# LAUREATE_FILE = "laureate_data.txt"

# def read_group_data():
#     group_choices = []
#     fr = open(GROUP_FILE, 'r')
#     for line in fr:
#         choice_lst = []
#         line = line.split(':')[1]
#         line = line.strip()
#         # print(line)
#         for elem_nobel in line.split(', '):
#             choice_lst.append(int(elem_nobel[1:]))
#         group_choices.append(choice_lst)
#     return group_choices

# def read_laureate_data():
#     laureate_choices = []
#     fr = open(LAUREATE_FILE, 'r')
#     for line in fr:
#         slot_lst = []
#         line = line.split(':')[1]
#         line = line.strip()
#         for slot in line.split(', '):
#             slot_lst.append(int(slot))
#         laureate_choices.append(slot_lst)
#     return laureate_choices

class CSP:
    def __init__(self, GROUP_CHOICES, LAUREATE_CHOICES):
        self.no_of_groups = len(GROUP_CHOICES)
        self.no_of_laureates = len(LAUREATE_CHOICES)
        self.groups_lst = list(GROUP_CHOICES)
        self.laureates_lst = []
        for lst in LAUREATE_CHOICES:
            self.laureates_lst.append(set(lst))
        self._create_graph()
    def _create_graph(self):
        # Laureates numbers are 0-indexed in the graph.
        # Undirected graph is created.
        self.constraint_graph = []
        for _ in range(self.no_of_laureates):
            self.constraint_graph.append(set())
        for group in self.groups_lst:
            for laureate_1 in group:
                for laureate_2 in group:
                    if laureate_1 == laureate_2:
                        continue
                    # print(laureate_1, group)
                    self.constraint_graph[laureate_1-1].add(laureate_2-1)

class State:
    def __init__(self, no_of_laureates):
        self.no_of_laureates = no_of_laureates
        self.assignment = [0]*no_of_laureates # As 0 means that the particular laureate is not assigned a slot till now.
    def is_assignment_complete(self):
        for elem in self.assignment:
            if elem == 0:
                return False
        return True
    def assign_value(self, var, value):
        self.assignment[var] = value # Assume var i.e. laureate is 0-indexed.
    def unassign_value(self, var):
        self.assignment[var] = 0 # Assume var i.e. laureate is 0-indexed.
        
def check_consistency(csp, state, var, value):
    """
    Check if var = value is consistent with the partial assignment in state.
    """
    for neighbor in csp.constraint_graph[var]: # Assume var i.e. laureate is 0-indexed.
        if state.assignment[neighbor] == value:
            return False
    return True

def complete_variable_ordering(variable_order, no_of_laureates):
    complete_variable_order = []
    for elem in variable_order:
        complete_variable_order.append(elem+1)
    for idx in range(no_of_laureates):
        if idx not in variable_order:
            complete_variable_order.append(idx+1)
    return complete_variable_order

def is_MRV_zero(csp):
    for lst in csp.laureates_lst:
        if len(lst) == 0:
            return True
    return False