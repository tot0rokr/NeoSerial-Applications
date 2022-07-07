from make_adjacency_matrix import make_matrix, change_list

from find_optimal_relay import find_relaies, verify_relaies, erase_redundant_relaies, add_essential_relaies

def status_check(status, adj, repeaters, relaies, prefix="error"):
    if not status:
        print("{}: repeaters: {}, relaies: {}".format(prefix, repeaters, relaies))
        #  for i, row in adj.items():
            #  print("{}: {}".format(i, row))
        print("")
        return True
    return False

#  PROBABILITY_MIN = 10
#  PROBABILITY_MAX = 100
#  PROBABILITY_INT = 10
#  NODE_NR_MIN = 5
#  NODE_NR_MAX = 50
#  NODE_NR_INT = 5
#  REPEATERS_MIN = 1
#  REPEATERS_MAX = 10
#  REPEATERS_ADD = 5
#  REPEATERS_ERASE = 10

PROBABILITY_MIN = 10
PROBABILITY_MAX = 100
PROBABILITY_INT = 5
NODE_NR_MIN = 5
NODE_NR_MAX = 50
NODE_NR_INT = 5
REPEATERS_MIN = 1
REPEATERS_MAX = 10
REPEATERS_ADD = 5
REPEATERS_ERASE = 5

if __name__ == "__main__":
    test_count = 0
    for probability in range(PROBABILITY_MIN, PROBABILITY_MAX, PROBABILITY_INT):
        print("probability: %d" % probability)
        for node_nr in range(NODE_NR_MIN, NODE_NR_MAX, NODE_NR_INT):
            print("node_nr: %d" % node_nr)
            mat = make_matrix(node_nr, probability)
            adj = change_list(mat)

            for repeaters in range(REPEATERS_MIN, REPEATERS_MAX):
                test_count += 1
                relaies = find_relaies(adj, repeaters)
                if len(relaies) == 0:
                    break
                status = verify_relaies(adj, relaies, repeaters)

                if status_check(status, adj, repeaters, relaies, "new"):
                    break

                for add_repeaters in range(REPEATERS_ADD):
                    test_count += 1
                    new_relaies = add_essential_relaies(adj, relaies, repeaters + add_repeaters + 1)
                    status = verify_relaies(adj, relaies, repeaters + add_repeaters + 1)
                    if status_check(status, adj, repeaters + add_repeaters, relaies, "add"):
                        break
                if not status:
                    break

                for erase_repeaters in range(min(REPEATERS_ERASE, repeaters + REPEATERS_ADD - 1)):
                    test_count += 1
                    erased_relaies = erase_redundant_relaies(adj, relaies, repeaters - erase_repeaters - 1)
                    status = verify_relaies(adj, relaies, repeaters - erase_repeaters - 1)
                    if status_check(status, adj, repeaters - erase_repeaters, relaies, "ers"):
                        break
                if not status:
                    break


                for add_repeaters in range(REPEATERS_ADD):
                    test_count += 1
                    new_relaies = add_essential_relaies(adj, relaies, repeaters + add_repeaters + 1)
                    status = verify_relaies(adj, relaies, repeaters + add_repeaters + 1)
                    if status_check(status, adj, repeaters + add_repeaters, relaies, "agn"):
                        break
                if not status:
                    break

    print("total test count:", test_count)

