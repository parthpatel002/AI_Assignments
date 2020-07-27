"""
@author: 2016A7PS0150P (Patel Parth)
"""

from utils import *

def compute_markov_blanket(graph, rev_graph, var):
    parents = rev_graph[var]
    children = graph[var]
    childrens_parents = []
    for child in children:
        childrens_parents.extend(rev_graph[child])
    markov_blanket = set(parents+children+childrens_parents)
    markov_blanket.add(var)
    # markov_blanket.discard(var)
    return markov_blanket

def eliminate_irrelevant_leaf_nodes(new_graph, query_or_evidence_vars):
    irrelevant_leaf_nodes = []
    for var in new_graph.keys():
        if (new_graph[var]==[]) and (var not in query_or_evidence_vars):
            irrelevant_leaf_nodes.append(var)
    for var in irrelevant_leaf_nodes:
        del new_graph[var]
    for var in irrelevant_leaf_nodes:
        for key in new_graph.keys():
            if var in new_graph[key]:
                new_graph[key].remove(var)
    return new_graph
    
def reverse_graph(var_set, graph):
    rev_graph = dict()
    for var in var_set:
        rev_graph[var] = []
    for var in graph.keys():
        for nbr in graph[var]:
            rev_graph[nbr].append(var)
    return rev_graph

def variable_elimination(graph, query_or_evidence_vars):
    new_graph = dict()
    for var in graph.keys():
        new_graph[var] = list(graph[var])
    while True:
        prev_len = len(new_graph)
        new_graph = eliminate_irrelevant_leaf_nodes(new_graph, query_or_evidence_vars)
        if prev_len == len(new_graph):
            break
    new_var_set = list(new_graph.keys())
    new_rev_graph = reverse_graph(new_var_set, new_graph)
    return new_var_set, new_graph, new_rev_graph

def recurse(bayesian_net, involved_vars, topological_order):
    if len(topological_order) == 0:
        return decimal.Decimal(1.0)
    first_var = topological_order[0]
    # print("First Var:", first_var)
    rest_vars = topological_order[1:]
    if first_var in involved_vars:
        conditional_vars = bayesian_net.rev_graph[first_var]
        conditional_vars_list = []
        for conditional_var in conditional_vars:
            if involved_vars[conditional_var] == 0:
                conditional_vars_list.append('~'+conditional_var)
            else:
                conditional_vars_list.append(conditional_var)
        # print("conditional_vars_list: ", conditional_vars_list)
        if involved_vars[first_var] == 0:
            p1 = bayesian_net.cpt[('~'+first_var, frozenset(conditional_vars_list))]
        else:
            p1 = bayesian_net.cpt[(first_var, frozenset(conditional_vars_list))]
        p2 = recurse(bayesian_net, involved_vars, rest_vars)
        # print(p1*p2)
        return p1*p2
    else:
        sum = decimal.Decimal(0.0)
        conditional_vars = bayesian_net.rev_graph[first_var]
        conditional_vars_list = []
        for conditional_var in conditional_vars:
            if involved_vars[conditional_var] == 0:
                conditional_vars_list.append('~'+conditional_var)
            else:
                conditional_vars_list.append(conditional_var)
        # print("conditional_vars_list: ", conditional_vars_list)
        for first_var_value in range(2):
            if first_var_value == 0:
                p1 = bayesian_net.cpt[('~'+first_var, frozenset(conditional_vars_list))]
            else:
                p1 = bayesian_net.cpt[(first_var, frozenset(conditional_vars_list))]
            involved_vars.update({first_var:first_var_value})
            p2 = recurse(bayesian_net, involved_vars, rest_vars)
            del involved_vars[first_var]
            sum += (p1*p2)
        # print(sum)
        return sum

def calculate(bayesian_net, involved_vars):
    """
    involved_vars - A dictionary with key-val pair as (variable, 0/1), where 0 means negative literal and 1 means positive literal
    """
    topological_order = topological_ordering(bayesian_net.var_set, bayesian_net.graph)
    # print("Topological Order: ", topological_order)
    return recurse(bayesian_net, involved_vars, topological_order)

def compute_probability(bayesian_net, query_vars, evidence_vars):
    """
    query_vars - A dictionary with key-val pair as (variable, 0/1), where 0 means negative literal and 1 means positive literal
    evidence_vars - A dictionary with key-val pair as (variable, 0/1), where 0 means negative literal and 1 means positive literal
    """
    if len(query_vars) == 0:
        return None
    query_or_evidence_vars = set()
    for query_var in query_vars.keys():
        query_or_evidence_vars.add(query_var)
    for evidence_var in evidence_vars.keys():
        query_or_evidence_vars.add(evidence_var)
    new_var_set, new_graph, new_rev_graph = variable_elimination(bayesian_net.graph, query_or_evidence_vars)
    # print(new_var_set)
    new_bayesian_net = create_bayesian_network(new_var_set, new_graph, new_rev_graph, bayesian_net.cpt)
    if len(evidence_vars) == 0:
        return calculate(new_bayesian_net, query_vars)
    else:
        involved_vars = dict(query_vars)
        involved_vars.update(evidence_vars)
        # print("involved_vars: ", involved_vars)
        p1 = calculate(new_bayesian_net, involved_vars)
        # print("evidence_vars: ", evidence_vars)
        p2 = calculate(new_bayesian_net, evidence_vars)
        # print("p1: ", str(p1))
        # print("p2: ", str(p2))
        return (p1/p2)

# if __name__ == "__main__":
    # var_set, graph, rev_graph, cpt = read_input_file('input1.txt')
    # print(compute_markov_blanket(graph, rev_graph, 'A'))
    # bayesian_net = create_bayesian_network(var_set, graph, rev_graph, cpt)
    # print(str(compute_probability(bayesian_net, {'A':1}, {})))
    # print(str(compute_probability(bayesian_net, {'D':1, 'A':1, 'L':1}, {'R':0, 'X':1, 'P':1, 'O':0})))
    # print(str(compute_probability(bayesian_net, {'F':1, 'R':1}, {'A':0, 'P':0})))
    # print(str(compute_probability(bayesian_net, {'D':1}, {})))
    # print(str(compute_probability(bayesian_net, {'D':1}, {'P':1})))
    # print(str(compute_probability(bayesian_net, {'A':1}, {'C':0, 'Y':0})))
    # print(str(compute_probability(bayesian_net, {'A':1, 'D':1}, {'O':1, 'R':0, 'P':1})))
    #----------------------------------------------------------------------------------------
    # bayesian_net = Bayesian_Network('input3.txt')
    # print(str(compute_probability(bayesian_net, {'C':0}, {})))
    # print(str(compute_probability(bayesian_net, {'C':1}, {'R':1, 'S':1, 'W':0})))
    #----------------------------------------------------------------------------------------
    # bayesian_net = Bayesian_Network('input2.txt')
    # print(str(compute_probability(bayesian_net, {'B':1}, {'J':1, 'M':1})))
    # print(str(compute_probability(bayesian_net, {'B':0}, {'J':1, 'M':1})))
    # print(str(compute_probability(bayesian_net, {'A':1, 'J':1, 'M':1, 'B':0, 'E':0}, {})))
    ## print(str(compute_probability(bayesian_net, {'A':1, 'J':1, 'M':1, 'B':0, 'E':0}, {'E':1})))