import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys

from make_adjacency_matrix import make_matrix, change_list

from find_optimal_relay import find_relaies, verify_relaies

NODE_NR = 15
PROBABILITY = 50
REPEATERS = 2

if __name__ == "__main__":
    mat = make_matrix(NODE_NR, PROBABILITY)
    adj = change_list(mat)
    print('-----------------------------------')
    for i, row in adj.items():
        print("{}: {}".format(i, row))
    print('-----------------------------------')
    G = nx.Graph(adj)
    d = dict(G.degree)
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, nodelist=d.keys(), with_labels=True)

    relaies = find_relaies(adj, REPEATERS)
    verify_relaies(adj, relaies, REPEATERS)
    print ("relaies: ", relaies)

    list(filter(lambda x: x in relaies, d))
    nx.draw_networkx_nodes(G, pos, nodelist=relaies, node_color="#FF1144")

    plt.axis('equal')
    file_name = "graph.png"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    plt.savefig(file_name)
