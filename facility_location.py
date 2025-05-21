from ortools.linear_solver import pywraplp

def read_input():
    line = list(map(int, input().split()))
    n_depot = line[0]
    n_gest = line[1]
    cost_depot = list(map(int, input().split()))
    capas = list(map(int, input().split()))
    demands = list(map(int, input().split()))
    distances = []
    for _ in range(n_depot):
        line = list(map(int, input().split()))
        distances.append(line)
    
     
    return n_depot, n_gest, cost_depot, capas, demands, distances


def solve_facility_location(n_depot, n_gest, cost_depot, capas, demands, distances, max_demand):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    y = [solver.BoolVar(f'y_{i}') for i in range(n_depot)]    
    x = [[solver.IntVar(0, max_demand, f'x_{i}_{j}') for j in range(n_gest)] for i in range(n_depot)]

    for i in range(n_depot):
        solver.Add(sum(x[i][j] for j in range(n_gest)) <= capas[i])

    for i in range(n_depot):
        for j in range(n_gest):
            solver.Add(x[i][j] <= y[i]*demands[j])

    for j in range(n_gest):
        solver.Add(sum(x[i][j] for i in range(n_depot)) <= demands[j])        

    Total_Cost = sum(y[i]*cost_depot[i] for i in range(n_depot)) + sum(distances[i][j]*x[i][j] for j in range(n_gest) for i in range(n_depot))    

    solver.Minimize(Total_Cost)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(Total_Cost.solution_value()))
    else:
        print("solution not found")    


if __name__=="__main__":
    n_depot, n_gest, cost_depot, capas, demands, distances = read_input()
    max_demand = max(demands)
    solve_facility_location(n_depot, n_gest, cost_depot, capas, demands, distances, max_demand)
