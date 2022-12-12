from make_adjacency_matrix import *

topo = change_list(make_matrix(9))
#  topo = [
    #  [5, 7, 8],
    #  [2, 5],
    #  [1, 3, 6, 7],
    #  [2, 4, 6, 8],
    #  [3, 7, 8],
    #  [1, 6, 0],
    #  [2, 3, 5, 7],
    #  [2, 4, 6, 8, 0],
    #  [3, 4, 7, 0]
#  ]

nr_node = len(topo)

cache = [dict() for i in range(nr_node)]

result = [[99] * nr_node for j in range(nr_node)]

steps = list()

def make_packet(src, dst, seq_num, hops):
    packet = [src, dst, seq_num, hops]
    return packet

def dequeue(prev, index, p):
    global cache
    global result
    p[3] += 1
    if p[1] == index:
        if result[p[0]][p[1]] > p[3]:
            result[p[0]][p[1]] = p[3]
        return
    else:
        if p[2] in cache[index] and cache[index][p[2]] < p[3]:
            print("%d: %d - %d is cached %d" % (index, p[0], p[1], p[3]))
            return
        else:
            cache[index][p[2]] = p[3]
            send_packet(prev, index, p)

def one_step(prev, index, p):
    def _step():
        dequeue(prev, index, p)
    return _step

def send_packet(prev, index, p):
    global topo
    global steps
    for n in topo[index]:
        if n != prev:
            print("%d to %d (%r)" % (index, n, p))
            p = make_packet(p[0], p[1], p[2], p[3])
            steps.append(one_step(index, n, p))

if __name__ == '__main__':
    seq_num = 0
    for i in range(nr_node):
        for j in range(nr_node):
            if i == j:
                result[i][j] = 0
                continue
            p = make_packet(i, j, seq_num, 0)
            seq_num += 1
            send_packet(-1, i, p)
    while len(steps) > 0:
        f = steps.pop(0)
        f()
    print("")
    for row in topo:
        print(row)
    print("")
    for row in result:
        print(row)
