from ortools.linear_solver import pywraplp

def read_input():
    line = list(map(int, input().split()))
    n = line[0]
    k = line[1]
    distances = []
    for _ in range(2*n+1):
        line = list(map(int, input().split()))
        distances.append(line)

    return n,k,distances

def solve_cbus_lp(n, k, distances):

    solver = pywraplp.Solver.CreateSolver("SCIP")
    x = [[solver.BoolVar(f'x_{i}_{j}') for j in range(2*n+1)] for i in range(2*n +1)]
    
    for i in range(2*n + 1):
        solver.Add(x[i][i] == 0)

    solver.Add(sum(x[0][i] for i in range(n+1)) ==1)
    solver.Add(sum(x[i][0] for i in range(n,2*n+1)) == 1)

    for i in range(1, 2*n+1):
        solver.Add(sum(x[i][j] for j in range(2*n+1)) == 1)
        solver.Add(sum(x[j][i] for j in range(2*n+1)) == 1)

    u = [solver.IntVar(0,2*n, f'u_{i}') for i in range(2*n+1)]
    solver.Add(u[0] == 0)

    for i in range(2*n+1):
        for j in range(1, 2*n+1):
             solver.Add(u[j] >= u[i]+1 - 2*n*(1 - x[i][j]))
             solver.Add(u[j] <= u[i]+1 + 2*n*(1 - x[i][j]))

    for j in range(1,n+1):
        solver.Add(u[n+j] >= u[j]+1)

    c = [solver.IntVar(0,n,f'c_{i}') for i in range(2*n+1)]
    
    solver.Add(c[0] == 0)
    for i in range(2*n+1):
        for j in range(1,n+1):
            solver.Add(c[j] >= c[i] + 1 - n*(1 - x[i][j]))
            solver.Add(c[j] <= c[i] + 1 + n*(1 - x[i][j]))

    for i in range(1, 2*n+1):
        for j in range(n+1, 2*n+1):
            solver.Add(c[j]<= c[i] -1 + n*(1 - x[i][j]))
            solver.Add(c[j] >= c[i] -1 - n*(1 - x[i][j]))

    for i in range(1, 2*n+1):
        solver.Add(c[i] <=k)

    TotalCost = sum(distances[i][j]*x[i][j] for j in range(2*n+1) for i in range(2*n+1))
    solver.Minimize(TotalCost)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(TotalCost.solution_value()))
    else:
        print("solution not found")                        
    



if __name__ =="__main__":
   n , k, distances = read_input()
   solve_cbus_lp(n,k, distances)