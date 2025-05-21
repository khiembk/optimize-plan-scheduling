from ortools.linear_solver import pywraplp

def read_input():
    line = list(map(int, input().split()))
    n = line[0]
    degree = line[1]
    distances = []
    for _ in range(n):
        line = list(map(int, input().split()))
        distances.append(line)

    return n, degree, distances

def better_solve_spanning_tree(n, degree, distances):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    x = [[solver.BoolVar(f'x_{i}_{j}') for j in range(n)] for i in range(n)]

    for i in range(n):
       for j in range(n):
           if i==j or distances[i][j] == 0:
                solver.Add(x[i][j] == 0)

    for i in range(n):
        solver.Add(sum(x[i][j] for j in range(n)) + sum(x[j][i] for j in range(n)) >=1)
        solver.Add(sum(x[i][j] for j in range(n)) + sum(x[j][i] for j in range(n)) <=degree)

    solver.Add(sum(x[i][j] for j in range(n) for i in range(n)) == n-1)

    TotalCost = sum(x[i][j]*distances[i][j] for j in range(n) for i in range(n))
    
    solver.Minimize(TotalCost)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(TotalCost.solution_value()))
    else:
        print("solution not found")        










def solve_spanning_tree(n, degree, distances, start):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    x = [[solver.BoolVar(f'x_{i}_{j}') for j in range(n)] for i in range(n)]
    u = [solver.IntVar(0, n-1, f'u_{i}') for i in range(n)]
    
    solver.Add(u[start] == 0)
    for i in range(n):
        for j in range(n):
            if i==j or distances[i][j] == 0: 
                  solver.Add(x[i][j] == 0)
    
    solver.Add(sum(x[j][start] for j in range(n)) == 0)

    for i in range(n):
        if i != start:
            solver.Add(sum(x[j][i] for j in range(n)) == 1)

    for i in range(n):
        for j in range(n):
            solver.Add(u[j] >= u[i] + 1 - n*(1 - x[i][j]))        
    
    for i in range(n):
        solver.Add(sum(x[i][j] for j in range(n)) + sum(x[j][i] for j in range(n)) <= degree)

    Total_Cost = sum(x[i][j]*distances[i][j] for j in range(n) for i in range(n))

    solver.Minimize(Total_Cost)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(Total_Cost.solution_value()))
        return int(Total_Cost.solution_value())
    else:
        print("Solution not found")        
            



if __name__ =="__main__":
   n, degree, distances = read_input()
   better_solve_spanning_tree(n, degree, distances)
#    cost =[0]*n
#    for i in range(n):
#        cost[i] = solve_spanning_tree(n,degree,distances,i)

#    min_cost = min(cost)
#    print("Total Min", min_cost)    