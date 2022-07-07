import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys

from make_adjacency_matrix import make_matrix, change_list

from find_optimal_relay import find_relaies, verify_relaies, erase_redundant_relaies, add_essential_relaies

NODE_NR = 20
PROBABILITY = 30
REPEATERS = 1

if __name__ == "__main__":
    plt.figure(figsize=(10, 10))

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

    nx.draw_networkx_nodes(G, pos, nodelist=relaies, node_color="#FF1144")

    #  if REPEATERS > 1:
        #  erased_relaies = erase_redundant_relaies(adj, relaies, REPEATERS - 1)
        #  verify_relaies(adj, relaies, REPEATERS - 1)
        #  print ("relaies: ", relaies)

        #  nx.draw_networkx_nodes(G, pos, nodelist=erased_relaies, node_color="#AA1144")

    #  if REPEATERS > 2:
        #  erased_relaies = erase_redundant_relaies(adj, relaies, REPEATERS - 2)
        #  verify_relaies(adj, relaies, REPEATERS - 2)
        #  print ("relaies: ", relaies)

        #  nx.draw_networkx_nodes(G, pos, nodelist=erased_relaies, node_color="#441144")

    new_relaies = add_essential_relaies(adj, relaies, REPEATERS + 1)
    verify_relaies(adj, relaies, REPEATERS + 1)
    print ("relaies: ", relaies)

    nx.draw_networkx_nodes(G, pos, nodelist=new_relaies, node_color="#996699")

    new_relaies = add_essential_relaies(adj, relaies, REPEATERS + 2)
    verify_relaies(adj, relaies, REPEATERS + 2)
    print ("relaies: ", relaies)

    nx.draw_networkx_nodes(G, pos, nodelist=new_relaies, node_color="#EEBBEE")

    plt.axis('equal')
    file_name = "graph.png"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    plt.savefig(file_name)
