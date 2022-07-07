import copy

def find_relay(adj, group):
    target = None
    for i in adj.keys():
        if len(adj[i]) <= 0:
            continue
        if len(group) > 0:
            if i not in group:
                continue
        if target is None or len(adj[target]) < len(adj[i]):
            target = i
    return target

def find_relaies(adj, repeaters=1, capacity="TODO"):
    copied = copy.deepcopy(adj)
    relaies = []
    connected = {}
    group = set()
    for n in adj.keys():
        connected[n] = 0

    while len(list(filter(lambda x: len(copied[x]) > 0, copied.keys()))):
        target = find_relay(copied, group)
        # adj is clean or severed networks
        if target is None:
            return []
        relaies.append(target)
        target_connected = copied[target]
        del copied[target]
        for n in target_connected:
            group.add(n)
            connected[n] += 1
            if connected[n] >= min(repeaters, len(adj[n])):
                for row in copied.values():
                    if n in row:
                        row.remove(n)

    return relaies


def erase_redundant_relaies(adj, relaies, repeaters=1):
    def get_parent(parents, node):
        if parents[node] == node:
            return node
        else:
            parents[node] = get_parent(parents, parents[node])
            return parents[node]
    def union_parent(parents, a, b):
        a = get_parent(parents, a)
        b = get_parent(parents, b)
        if a < b:
            parents[b] = a
        else:
            parents[a] = b
    sorted_relaies = sorted(relaies, key=lambda x: len(adj[x]))
    erased_relaies = []
    for target in sorted_relaies:
        # Check that peripheral nodes don't need relay.
        check_erase = True
        for n in adj[target]:
            if len(set(adj[n]) & set(relaies)) - 1 < repeaters:
                check_erase = False
                break
        if not check_erase:
            continue

        # Check severed between networks
        adj_relaies = {}
        for r in relaies:
            adj_relaies[r] = list(filter(lambda x: x in relaies and x != target, adj[r]))
        del adj_relaies[target]

        parents_relaies = dict(zip(relaies, relaies))
        del parents_relaies[target]
        for relay, nodes in adj_relaies.items():
            for node in nodes:
                union_parent(parents_relaies, relay, node)

        for relay in adj_relaies.keys():
            get_parent(parents_relaies, relay)

        parents_relaies_list = list(parents_relaies.items())
        if not len(list(filter(lambda x: x[1] == parents_relaies_list[0][1], parents_relaies_list))) == len(parents_relaies_list):
            continue

        # Erase target
        erased_relaies.append(target)
        relaies.remove(target)
        sorted_relaies.remove(target)

    return erased_relaies

## v1

#  def find_relaies(adj, capacity="TODO"):
    #  copied = copy.deepcopy(adj)
    #  relaies = []
    #  connected = []

    #  while len(connected) < len(adj):
        #  target = find_relay(copied)
        #  relaies.append(target)
        #  connected.append(target)
        #  for n in copied[target]:
            #  connected.append(n)
            #  for row in copied.values():
                #  if n in row:
                    #  row.remove(n)
        #  for row in copied.values():
            #  if target in row:
                #  row.remove(target)
        #  del copied[target]

    #  return relaies

def verify_relaies(adj, relaies, repeaters):
    if len(relaies) == 0:
        return True
    # Each nodes connect to enough repeaters
    relaies_set = set(relaies)
    for n in adj.keys():
        connected_repeaters = len(set(adj[n]) & relaies_set)
        if connected_repeaters < min(repeaters, len(adj[n])):
            print("%d is not completed" % n)
            print("adj", adj[n], "relaies", relaies)
            print("connected", connected_repeaters, "repeaters", repeaters, "len", len(adj[n]))
            return False

    # Repeaters connected to each other
    varified_relaies = []
    varified_relaies.append(relaies[0])
    for i in varified_relaies:
        connected = list(set(adj[i]) & relaies_set)
        for n in connected:
            if n not in varified_relaies:
                varified_relaies.append(n)
    if len(varified_relaies) != len(relaies):
        print("repeaters are disconnected", relaies, varified_relaies)
        return False

    return True
