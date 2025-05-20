from ortools.linear_solver import pywraplp

def read_input():
    line = list(map(int, input().split()))
    n = line[0]
    k = line[1]
    q = line[2]
    demand = list(map(int, input().split()))
    demand = [0] + demand
    distances = []
    for i in range(n+1): 
        line = list(map(int, input().split()))
        distances.append(line)
    
    return n,k,q,demand, distances

def solve_cvr_lp(n , cars, capa, demand, distances):

    solver = pywraplp.Solver.CreateSolver('SCIP')
    x = [[[solver.BoolVar(f'x_{i}_{j}_{k}') for k in range(cars)] for j in range(n+1)] for i in range(n+1)]
    
    
    for i in range(n+1):
        for j in range(n+1):
            solver.Add(sum(x[i][j][k] for k in range(cars)) <=1)

    for i in range(1,n+1):
        solver.Add(sum(x[j][i][k] for j in range(n+1) for k in range(cars)) == 1)

    for k in range(cars):
        for i in range(n+1):
            solver.Add(sum(x[j][i][k] for j in range(n+1)) - sum(x[i][j][k] for j in range(n+1))== 0)     

    for k in range(cars):
        for i in range(n+1):
            solver.Add(x[i][i][k] == 0)

    solver.Add(sum(x[0][j][k] for j in range(1,n+1) for k in range(cars)) <=cars)
    
    max_c = sum(demand[i] for i in range(n+1))
    c = [solver.IntVar(0, max_c, f'c_{j}') for j in range(0, n+1)]
   
    solver.Add(c[0] == 0)
    
    for i in range(n+1):
        for j in range(1,n+1):
            if (i!=j):
                solver.Add(c[j] >= c[i] + demand[j]  - max_c*(1 - sum(x[i][j][k] for k in range(cars)))) 
    
    for i in range(1, n+1):
        solver.Add(c[i] <= capa)

    Total_cost = sum(distances[i][j]*(sum(x[i][j][k] for k in range(cars))) for i in range(n+1) for j in range(n+1))            
    
    solver.Minimize(Total_cost)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(Total_cost.solution_value()))
    else:
        print("solution not found")    
    return 0

if __name__=="__main__":
    n,k,q,demand, distances = read_input()
    solve_cvr_lp(n, k, q, demand, distances)