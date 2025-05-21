from ortools.sat.python import cp_model

def read_input():
    line = list(map(int, input().split()))
    num_teachers ,num_cources = line[0], line[1]
    specs = []
    conflics = []
    for _ in range(num_teachers):
        line = list(map(int, input().split()))
        line = line[1:]
        new_line = [ele-1 for ele in line]
        specs.append(new_line)

    k = int(input())
    for _ in range(k):
        line = list(map(int, input().split()))
        new_line = [ele-1 for ele in line]
        conflics.append(new_line)

    return num_teachers, num_cources,specs, conflics    


def solve_bca_cp(num_teachers, num_cources, specs, conflics):
    model = cp_model.CpModel()
    x = [model.NewIntVar(0, num_teachers-1, f'x_{i}') for i in range(num_cources)]
    y = [model.NewIntVar(0, num_cources, f'y_{i}') for i in range(num_teachers)]
    assign  = [[model.NewBoolVar(f'assign_{i}_{j}') for j in range(num_cources)] for i in range(num_teachers)]

    
    for i in range(num_teachers):
        for j in range(num_cources):
            if j not in specs[i]:
                model.Add(x[j]!= i)

    for conflic in conflics:
        c1 = conflic[0]
        c2 = conflic[1]
        model.Add(x[c1] != x[c2])
    
    
     
    for i in range(num_teachers):
        for j in range(num_cources):
            model.Add(x[j] == i).OnlyEnforceIf(assign[i][j])
            model.Add(x[j] != i).OnlyEnforceIf(assign[i][j].Not())

    for i in range(num_teachers):
        model.Add(y[i] == sum(assign[i][j] for j in range(num_cources))) 
    
    max_load = model.NewIntVar(0, num_cources, 'max_load')
    for i in range(num_teachers):
        model.Add(max_load >= y[i])
    model.Minimize(max_load)
    solver = cp_model.CpSolver()
    status  = solver.Solve(model)
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(int(solver.Value(max_load)))
    else:
        print("Solution not found")    
            

if __name__ == "__main__":
    num_teachers, num_cources,specs, conflics  = read_input()
    solve_bca_cp(num_teachers, num_cources, specs, conflics)