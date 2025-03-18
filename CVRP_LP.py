from ortools.init.python import init
from ortools.linear_solver import pywraplp

def get_data():
    n,k,q = map(int, input().split())
    note_capa = line = list(map(int, input().split()))
    distance = []
    for _ in range(n):
        line = list(map(int, input().split()))
        distance.append(line)

    return n,k,q, distance

def Solve_CVRP(n,k,q, distance):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return -1
    
    
    x = [[solver.BoolVar(f'x_{t}_{c}') for c in range(n+1)] for t in range(n+1)]
    
    
    for c in range(n):
        solver.Add(sum(x[t][c] for t in range(1,n)) == 1)
    
   
    for t in range(m):
        for c in range(n):
            if c + 1 not in preferences[t]:  # Course indices are 1-based in input
                solver.Add(x[t][c] == 0)
    
   
    for c1, c2 in conflicts:
        for t in range(m):
            solver.Add(x[t][c1 - 1] + x[t][c2 - 1] <= 1)
    
   
    max_load = solver.IntVar(0, n, 'max_load')
    for t in range(m):
        solver.Add(sum(x[t][c] for c in range(n)) <= max_load)
    solver.Minimize(max_load)
    
    # Solve model
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        return int(max_load.solution_value())
    else:
        return -1

def main():
    n,k,q,distance = get_data()

if __name__ == "__main__":
    main()     
    

