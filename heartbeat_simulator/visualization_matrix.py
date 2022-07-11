import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys

from make_adjacency_matrix import make_matrix, change_list

from find_optimal_relay import find_relaies
from find_optimal_relay import verify_relaies
from find_optimal_relay import erase_redundant_relaies
from find_optimal_relay import add_essential_relaies
from find_optimal_relay import erase_terminal_relaies

import random

NODE_NR = 50
PROBABILITY = 40
REPEATERS = 10
ERASE = 9
ADD = 5

__adj = {
    1: [2],
    2: [1, 3, 4],
    3: [2, 4, 5, 6, 7],
    4: [2, 3, 8, 9],
    5: [3, 6],
    6: [3, 5],
    7: [3],
    8: [4, 9, 10, 11, 12, 13, 14],
    9: [4, 8, 10],
    10: [8, 9, 13],
    11: [8, 12, 15, 16],
    12: [8, 11, 17, 18],
    13: [8, 10, 14, 19, 20, 21],
    14: [8, 13],
    15: [11],
    16: [11],
    17: [12],
    18: [12],
    19: [13, 20],
    20: [13, 19, 21, 22, 23],
    21: [13, 20, 24],
    22: [20],
    23: [20],
    24: [21]
}

if __name__ == "__main__":
    plt.figure(figsize=(10, 10))

    mat = make_matrix(NODE_NR, PROBABILITY)
    adj = change_list(mat)
    #  adj = __adj
    print('-----------------------------------')
    for i, row in adj.items():
        print("{}: {}".format(i, row))
    print('-----------------------------------')
    G = nx.Graph(adj)
    d = dict(G.degree)
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, nodelist=d.keys(), with_labels=True)

    relaies = find_relaies(adj, REPEATERS)
    print ("relaies: ", relaies)
    verify_relaies(adj, relaies, REPEATERS)

    nx.draw_networkx_nodes(G, pos, nodelist=relaies, node_color="#FF1144")

    for i in range(1, min(REPEATERS, ERASE)):
        erased_relaies = erase_redundant_relaies(adj, relaies, REPEATERS - i)
        relaies = list(set(relaies) - set(erased_relaies))
        print ("relaies: ", relaies)
        verify_relaies(adj, relaies, REPEATERS - i)
        color = "#%06X" % random.randint(1, 0xFFFFFF)
        nx.draw_networkx_nodes(G, pos, nodelist=erased_relaies, node_color=color)

    for i in range(1, ADD):
        new_relaies = add_essential_relaies(adj, relaies, REPEATERS + i - min(REPEATERS, ERASE) + 1)
        relaies += new_relaies
        print ("relaies: ", relaies)
        verify_relaies(adj, relaies, REPEATERS + i - min(REPEATERS, ERASE) + 1)
        color = "#%06X" % random.randint(1, 0xFFFFFF)
        nx.draw_networkx_nodes(G, pos, nodelist=new_relaies, node_color=color)

    erased_relaies = erase_terminal_relaies(adj, relaies)
    relaies = list(set(relaies) - set(erased_relaies))
    print ("relaies: ", relaies)
    verify_relaies(adj, relaies + erased_relaies, REPEATERS - min(REPEATERS, ERASE) + ADD)
    color = "#%06X" % random.randint(1, 0xFFFFFF)
    nx.draw_networkx_nodes(G, pos, nodelist=erased_relaies, node_color=color)

    plt.axis('equal')
    file_name = "graph.png"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    plt.savefig(file_name)
