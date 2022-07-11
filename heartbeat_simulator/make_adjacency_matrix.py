import random

def make_matrix(size, probability=50):
    if not 0 <= probability <= 100:
        raise IndexError("0 <= probability <= 100")
    mat = [[0] * size for _ in range(size)]
    for i in range(size):
        col = []
        for j in range(i):
            temp = random.randrange(0, 101)
            mat[i][j] = 1 if temp > (100 - probability) else 0
            mat[j][i] = mat[i][j]
    return mat

def change_list(mat):
    adj_list = {}
    for i in range(len(mat)):
        arr = []
        for j in range(len(mat[i])):
            if mat[i][j] > 0:
                arr.append(j)
        adj_list[i] = arr
    return adj_list

if __name__ == '__main__':
    mat = make_matrix(10)
    for row in mat:
        print (row)
    print("")
    adj_list = change_list(mat)
    for row in adj_list.values():
        print (row)
