import copy
import numpy as np
next_value = 1


def myrand():
    global next_value
    next_value = (((next_value * 1103515245) % 18446744073709551616) + 12345) % 18446744073709551616
    return (next_value / 65536) % 4294967296


def asign_label(G, edge, p=0.5):
    # Labels are the same, nothing happen
    if G.label[edge[0]] == G.label[edge[1]]:
        return G

    # Node 0 is zealot => 0 persuade
    if G.zea[edge[0]] == 0 and G.zea[edge[1]] == 1:
        n = 0
    # Node 1 is zealot => 1 persuade
    elif G.zea[edge[0]] == 1 and G.zea[edge[1]] == 0:
        n = 1
    # Nodes 0 and 1 is not zealot
    elif G.zea[edge[0]] == 1 and G.zea[edge[1]] == 1:
        # Nodes 0 and 1 are known => random choice
        if G.label[edge[0]] != p and G.label[edge[1]] != p:
            n = int(myrand() % 2)
        # node 0 is known => 0 persuade
        elif G.label[edge[0]] != 0.5 and G.label[edge[1]] == p:
            n = 0
        # node 0 is known => 0 persuade
        elif G.label[edge[0]] == 0.5 and G.label[edge[1]] != p:
            n = 1
        # Labels are the same - unknown, nothing happen
        else:
            return G
    # Unexpected error happened
    else:
        return G

    node = edge[n]

    G.label[edge[abs(int(n) - 1)]] = G.label[node]

    return G


def list_of_edges(G):
    return G.edge_indices()


def voter_model_realisation(G, max_iteration=6, epsilon=0.03):
    m = len(G.get_edges())

    L = 0.01
    list_edges = G.edge_indices()
    initial_state = copy.deepcopy(np.array(G.label))

    changes_history = []
    stopping_time = int(1 / L)

    for t in range(int(1 / L)):
        for i in range(int(2 * 10 ** max_iteration * L)):
            edge = list_edges[int(myrand() % m)]
            G = asign_label(G, edge)

        current_state = np.array(G.label)
        changes = sum((initial_state != current_state) * 1) / int(10 ** max_iteration * L)
        changes_history.append(changes)

        if changes < epsilon:
            stopping_time = t
            break

        initial_state = copy.deepcopy(current_state)

    x = np.arange(len(changes_history))
    unknown = sum((np.array(G.label) == 0.5) * 1)
    return changes_history, x, stopping_time, unknown
