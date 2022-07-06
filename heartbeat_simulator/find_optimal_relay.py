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
        relaies.append(target)
        target_connected = copied[target]
        del copied[target]
        for n in target_connected:
            group.add(n)
            connected[n] += 1
            if connected[n] >= min(repeaters, len(adj[target])):
                for row in copied.values():
                    if n in row:
                        row.remove(n)

    return relaies

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
    # Each nodes connect to enough repeaters
    relaies_set = set(relaies)
    for n in adj.keys():
        connected_repeaters = len(set(adj[n]) & relaies_set)
        if connected_repeaters < min(repeaters, len(adj[n])):
            print("%d is not completed" % n)
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
