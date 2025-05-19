# """"""
# Given a network which is a directed graph G = (V,E). Each directed edge (i,j) has length c(i,j).
# Find two edge-disjoint paths from 1 to n (two paths that do not have common edges) such that the sum of lengths of the two paths is minimal.

# Input
# Line 1: contains 2 positive integers n and m (1 <= n,m <= 30)
# Line i+1 (i = 1, 2, . . ., m): contains 3 positive integers u, v, c in which w is the length of the directed edge(u,v)

# Output
# Write the sum of lengths of thw two edge-disjoint paths found, or write NOT_FEASIBLE if no solution found.
# """"""

def read_input():
    line = list(map(int, input().split()))
    n, m = line[0], line[1]
    edges = []
    for i in range(m):
        line = list(map(int, input().split()))
        edges.append(line)

    return n,m, edges   


def main():
    n, m , edges = read_input()
    return 0

if __name__ == "__main__":
    main()    