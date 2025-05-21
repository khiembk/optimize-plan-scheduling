from ortools.linear_solver import pywraplp

def read_input():
    line = list(map(int, input().split()))
    n = line[0]
    m = line[1]
    start = line[2]-1
    time_limit = line[3]
    #############################################
    costs = [[0]*n for _ in range(n)] 
    times = [[0]*n for _ in range(n)]
    #############################################
    for _ in range(m):
        line = list(map(int, input().split()))
        n1 = line[0]-1
        n2 = line[1]-1
        times[n1][n2] = line[2]
        costs[n1][n2] = line[3]
        times[n2][n1] = line[2]
        costs[n2][n1] = line[3]  

   
    return n,start,time_limit, times, costs

def solve_broardCast(n,start,time_limit ,times, costs):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x = [[solver.BoolVar(f'x_{i}_{j}') for j in range(n)] for i in range(n)]
    Max_time = sum(times[i][j] for i in range(n) for j in range(n))
    t = [solver.IntVar(0, Max_time, f't_{j}') for j in range(n)]
    

    for i in range(n):
        for j in range(n):
           if i==j or costs[i][j] == 0:
                   solver.Add(x[i][j] == 0)

    for i in range(0,n):
        if i != start :
           solver.Add(sum(x[j][i] for j in range(n)) == 1)

    for i in range(n):
        for j in range(n):
            if j != start:
              solver.Add(t[j] >= t[i] + times[i][j] - Max_time*(1 - x[i][j]))  
              solver.Add(t[j] <= t[i] + times[i][j] + Max_time*(1 - x[i][j]))
    
    solver.Add(t[start] == 0)
    for i in range(n):
        if i!= start:
           solver.Add(t[i] <= time_limit)

    Total_cost = (sum(x[i][j]*costs[i][j] for j in range(n) for i in range(n)))

    solver.Minimize(Total_cost)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(Total_cost.solution_value()))
    else:
        print("Solution not found")                    
          
        
    return 0

if __name__ =="__main__":
    n,start,time_limit ,times, costs = read_input()
    solve_broardCast(n,start,time_limit ,times, costs)
