# """"""
# Given a network which is a directed graph G = (V,E). Each directed edge (i,j) has length c(i,j).
# Find two edge-disjoint paths from 1 to n (two paths that do not have common edges) such that the sum of lengths of the two paths is minimal.

# Input
# Line 1: contains 2 positive integers n and m (1 <= n,m <= 30)
# Line i+1 (i = 1, 2, . . ., m): contains 3 positive integers u, v, c in which w is the length of the directed edge(u,v)

# Output
# Write the sum of lengths of thw two edge-disjoint paths found, or write NOT_FEASIBLE if no solution found.
# """"""
from ortools.linear_solver import pywraplp
def read_input():
    line = list(map(int, input().split()))
    n, m = line[0], line[1]
    distances = [[0] * n for _ in range(n)]
    for i in range(m):
        line = list(map(int, input().split()))
        #print("current line: ", line)
        node1 = line[0]-1
        node2 = line[1]-1
        dis = line[2]
        distances[node1][node2] = dis

    return n,m, distances   

def solve_minimal_length_edge(n,m, distances):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    x = [[solver.BoolVar(f'x_{i}_{j}') for i in range(n)] for j in range(n)]
    y = [[solver.BoolVar(f'y_{i}_{j}') for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(n):
            solver.Add(x[i][j] + y[i][j] <=1)
            if (distances[i][j] == 0):
                solver.Add(x[i][j] == 0)
                solver.Add(y[i][j] == 0)
    for i in range(n):
        solver.Add(x[i][i] == 0)
        solver.Add(y[i][i] == 0)
    for i in range(1, n-1):
        solver.Add(sum(x[i][j] for j in range(n)) <=1)
        solver.Add(sum(x[j][i] for j in range(n)) - sum(x[i][j] for j in range(n)) == 0)
        solver.Add(sum(y[i][j] for j in range(n)) <=1)
        solver.Add(sum(y[j][i] for j in range(n))  - sum(y[i][j] for j in range(n)) == 0)
    
    solver.Add(sum(x[0][j] for j in range(n)) ==1)
    solver.Add(sum(x[j][n-1] for j in range(n)) ==1)
    solver.Add(sum(y[0][j] for j in range(n)) ==1)
    solver.Add(sum(y[j][n-1] for j in range(n)) ==1)
    
    u = [solver.IntVar(0, n, f'u_{i}') for i in range(n)] 
    v = [solver.IntVar(0, n, f'v_{i}') for i in range(n)]
    solver.Add(u[0] == 0)
    solver.Add(v[0] == 0) 
    for i in range(n): 
        for j in range(n):
            solver.Add(u[j] >= u[i] + 1 -n*(1 - x[i][j]))
            solver.Add(v[j] >= v[i] + 1 -n*(1 - y[i][j]))
            
    Total_cost = sum((x[i][j] + y[i][j])*distances[i][j] for i in range(n) for j in range(n))

    solver.Minimize(Total_cost)
    status  = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL: 
       print(int(Total_cost.solution_value()))
          
        
    else:
       print("NOT_FEASIBLE")
    return 0

def main():
    n, m , distances = read_input()
    #print("Distance: ", distances)
    solve_minimal_length_edge(n,m,distances)
    return 0

if __name__ == "__main__":
    main()    