from ortools.sat.python import cp_model

def solve_balanced_course_assignment(m, n, preferences, conflicts):
    model = cp_model.CpModel()
    x = [[model.NewBoolVar(f'x_{t}_{c}') for c in range(n)] for t in range(m)]
    #### constraints with subject 
    for c in range(n):
        model.Add(sum(x[t][c] for t in range(m)) == 1)
    ######     
    for t in range(m):
        for c in range(n):
            if c + 1 not in preferences[t]:  
                model.Add(x[t][c] == 0)

    
    for c1, c2 in conflicts:
        for t in range(m):
            model.Add(x[t][c1 - 1] + x[t][c2 - 1] <= 1)  

    # Objective: Minimize the maximum load per teacher
    max_load = model.NewIntVar(0, n, 'max_load')
    for t in range(m):
        model.Add(sum(x[t][c] for c in range(n)) <= max_load)
    
    model.Minimize(max_load)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        return solver.Value(max_load)
    else:
        return -1  # No feasible solution
   
def read_input():
    m, n = map(int, input().split())
    preferences = []
    for _ in range(m):
        line = list(map(int, input().split()))
        preferences.append(line[1:])
    
    k = int(input())
    conflicts = [tuple(map(int, input().split())) for _ in range(k)]
    return m,n, preferences,k,conflicts

def main():
    m,n,preferences,k, conflicts = read_input()
    solve_balanced_course_assignment(m,n,preferences,conflicts)

if __name__=="__main__":
    main()