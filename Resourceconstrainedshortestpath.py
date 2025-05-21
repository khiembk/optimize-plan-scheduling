from ortools.linear_solver import pywraplp

def read_input():
    line = list(map(int, input().split()))
    n = line[0]
    start = line[1]-1
    end = line[2] -1
    Min_resource = line[3]
    Max_resource = line[4]
    resources = []
    costs = []
    
    for _  in range(n):
        line = list(map(int, input().split()))
        resources.append(line)

    for _ in range(n):
        line = list(map(int, input().split()))
        costs.append(line)    
    
    return n, start, end, resources, costs, Max_resource, Min_resource

def solve_tsp_resurces(n,start,end, resources, costs, Max_resources, Min_resources):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    x = [[solver.BoolVar(f'x_{i}_{j}') for j in range(n)] for i in range(n)]
    u = [solver.IntVar(0, n-1, f'u_{i}') for i in range(n)]
    
    solver.Add(u[start] == 0)
    
    for i in range(n):
        for j in range(n):
            if i==j or costs[i][j] == 0: 
                solver.Add(x[i][j] == 0)

    solver.Add(sum(x[start][j] for j in range(n)) == 1)
    solver.Add(sum(x[j][start] for j in range(n)) == 0)
    solver.Add(sum(x[i][end] for i in range(n))==1)
    solver.Add(sum(x[end][j] for j in range(n)) == 0)

    for i in range(n):
        if (i!= start and i!= end):
            solver.Add(sum(x[i][j] for j in range(n)) -  sum(x[j][i] for j in range(n)) == 0)

    for i in range(n):
        if (i!= start and i!= end):
            solver.Add(sum(x[j][i] for j in range(n)) <=1)

    for i in range(n):
        for j in range(n):
            solver.Add(u[j] >= u[i] + 1 - n*(1 - x[i][j]))

    solver.Add(sum(x[i][j]*resources[i][j] for j in range(n) for i in range(n))<= Max_resources)
    solver.Add(sum(x[i][j]*resources[i][j] for j in range(n) for i in range(n))>= Min_resources)  
    Total_cost = sum(x[i][j]*costs[i][j] for j in range(n) for i in range(n))
    solver.Minimize(Total_cost)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(Total_cost.solution_value()))
    else:
        print("Solution not found")          
    return 0

if __name__ == "__main__":
    n,start,end, resources, costs, Max_resource, Min_resource = read_input()
    solve_tsp_resurces(n,start,end, resources, costs, Max_resource, Min_resource)
