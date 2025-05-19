from ortools.init.python import init
from ortools.linear_solver import pywraplp

def read_input():
    n = int(input())
    distances = []
    for i in range(n):
        line  = list(map(int, input().split()))
        distances.append(line)
    
    return n, distances

def solve_lp_tsp(n, distances):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    x = [[solver.BoolVar(f'x_{t}_{c}') for c in range(n)] for t in range(n)]
    
    for i in range(n): 
        solver.Add(x[i][i] == 0)

    for i in range(n):
        solver.Add(sum(x[i][j] for j in range(n))==1)
    
    for i in range(n):
        solver.Add(sum(x[j][i] for j in range(n))==1)

    u = [solver.NumVar(0, n, f'u_{i}') for i in range(n)]
    solver.Add(u[0] == 0)  # Start at position 0
    for i in range(1,n):
        for j in range(1,n):
            if i != j :
                solver.Add(u[j] >= u[i] + 1 - n * (1 - x[i][j]))  

    

    Total_cost = sum(x[i][j]*distances[i][j] for i in range(n) for j in range(n))
    solver.Minimize(Total_cost)

    status = solver.Solve()

    if status  == pywraplp.Solver.OPTIMAL: 
        
        path = []
        current = 0
        visited = set()
        while current not in visited:
            path.append(current)
            visited.add(current)
            for j in range(n):
                if x[current][j].solution_value() > 0.5:
                    current = j 
                    break
        city_tour = [idx + 1 for idx in path]
        # Output as required
        print(n)
        print(' '.join(map(str, city_tour)))
    else:
        print("Can't find solution")       


                  
    return 0

if __name__ == "__main__": 
   n, distances = read_input()
   solve_lp_tsp(n, distances)

