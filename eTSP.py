from ortools.linear_solver import pywraplp

def read_input():
    n = int(input())
    distances = []
    for _ in range(n):
        line = list(map(int, input().split()))
        distances.append(line)

    q = int(input())
    orders = []
    for _ in range(q):
        line = list(map(int, input().split()))
        new_line = [ele -1 for ele in line]
        orders.append(new_line)

    return n, distances, orders

def solve_eTSP(n, distances, orders):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    x = [[solver.BoolVar(f'x_{i}_{j}') for j in range(n)] for i in range(n)]

    for i in range(n):
        solver.Add(sum(x[i][j] for j in range(n)) == 1)

    for i in range(n):
        solver.Add(sum(x[j][i] for j in range(n)) == 1)

    for i in range(n):
        solver.Add(x[i][i] == 0)

    u = [solver.NumVar(0, n-1, f'u_{i}') for i in range(n)]
    solver.Add(u[0] == 0)

    for i in range(n):
        for j in range(1,n):
          if j!=i:
            solver.Add(u[j] >= u[i]+1 -n*(1 - x[i][j]))

    for order in orders:
        node1 = order[0]
        node2 = order[1]
        solver.Add(u[node2] >= u[node1]+1)

    Total_cost = sum(x[i][j]*distances[i][j] for i in range(n) for j in range(n))
    
    solver.Minimize(Total_cost) 
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL : 
        print(int(Total_cost.solution_value()))
    else:                           
        print("Solution not found")
        #print(int(Total_cost.solution_value()))
if __name__ == "__main__":
    n, distances, orders = read_input()
    solve_eTSP(n,distances,orders)