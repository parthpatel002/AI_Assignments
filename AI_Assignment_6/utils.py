"""
@author: 2016A7PS0150P (Patel Parth)
"""

from collections import deque
import decimal

class Bayesian_Network:
    def __init__(self, filename=""):
        if filename == "":
            self.var_set, self.graph, self.rev_graph, self.cpt = None, None, None, None
        else:
            self.var_set, self.graph, self.rev_graph, self.cpt = read_input_file(filename)

def create_bayesian_network(var_set, graph, rev_graph, cpt):
    bayesian_net = Bayesian_Network()
    bayesian_net.var_set = var_set
    bayesian_net.graph = graph
    bayesian_net.rev_graph = rev_graph
    bayesian_net.cpt = cpt
    return bayesian_net

def read_input_file(filename):
    """
    Returns:
    1. Set of variables.
    2. Directed graph as a dictionary.
    3. Reverse directed graph as a dictionary.
    4. Conditional Probability table(s) as a dictionary with key as (node, frozenset(conditioned nodes)).
    These 4 objects together represent the Bayesian Network.
    """
    fp = open(filename, 'r')
    lines = fp.readlines()
    # print(lines)
    var_set = set()
    for line in lines[:-1]:
        var_set.add(line.split(">>")[0].strip())
    graph = dict()
    rev_graph = dict()
    cpt = dict() # Conditional Probability Table(s)
    for var in var_set:
        graph[var] = []
        rev_graph[var] = []
    for line in lines[:-1]:
        # print(line)
        fields = line.strip().split('>>')
        node = fields[0].strip()
        nbrs = fields[1].strip().strip("[]")
        if nbrs == '':
            continue
        for nbr in nbrs.split(","):
            nbr = nbr.strip()
            graph[nbr].append(node)
            rev_graph[node].append(nbr)
    for line in lines[:-1]:
        fields = line.strip().split('>>')
        node = fields[0].strip()
        nbrs = rev_graph[node]
        if nbrs == []:
            probability = decimal.Decimal(fields[2].strip())
            cpt[(node, frozenset())] = probability
            cpt[("~"+node, frozenset())] = 1-probability
            continue
        no_bits = len(nbrs)
        bitmask='{0:0'+str(no_bits)+'b}'
        cnt = 0
        for prob in fields[2].strip().split(" "):
            probability = decimal.Decimal(prob.strip())
            bitstring = bitmask.format(cnt)
            condition_lst = []
            for idx, nbr in enumerate(nbrs):
                if bitstring[idx] == '0':
                    condition_lst.append('~'+nbr)
                else:
                    condition_lst.append(nbr)
            cpt[(node, frozenset(condition_lst))] = probability
            cpt[("~"+node, frozenset(condition_lst))] = 1-probability
            cnt += 1
    fp.close()
    return var_set, graph, rev_graph, cpt

def recursive_dfs(visited, graph, var, stack):
    for nbr in graph[var]:
        if nbr not in visited:
            recursive_dfs(visited, graph, nbr, stack)
    visited.add(var)
    stack.append(var)

def topological_ordering(var_set, graph):
    """
    DFS traversal to establish topological ordering of nodes
    """
    visited = set()
    stack = deque()
    for var in var_set:
        if var not in visited:
            recursive_dfs(visited, graph, var, stack)
    topological_order = []
    while len(stack) > 0:
        topological_order.append(stack.pop())
    return topological_order

# if __name__ == "__main__":
    # var_set, graph, rev_graph, cpt = read_input_file('input2.txt')
    # print(var_set)
    # print(graph)
    # print(rev_graph)
    # print(cpt)
    # print(cpt[('A', frozenset(['~B', 'E']))])
    # topological_order = topological_ordering(var_set, graph)
    # print(topological_order)
    #----------------------------------------------------------------------------------------
    # var_set, graph, rev_graph, cpt = read_input_file('input1.txt')
    # print(var_set)
    # print(graph)
    # print(rev_graph)
    # print(cpt)
    # topological_order = topological_ordering(var_set, graph)
    # print(topological_order)
    