from ortools.sat.python import cp_model
def read_input():
    num_teachers, num_cources = map(int,input().split())
    specialization = []
    for _ in range(num_teachers):
       line = list(map(int,input().split()))
       specialization.append(line[1:])
    num_conflicts = int(input())
    conflicts = []
    for _ in range(num_conflicts):
        cur_conflict = list(map(int,input().split()))
        conflicts.append(cur_conflict)
    return num_teachers, num_cources, specialization, conflicts

def sovle_BCA(num_teachers, num_cources, specialization, conflicts):
    model = cp_model.CpModel()
    x = [[model.NewBoolVar(f'x_{t}_{c}') for c in range(num_cources)]for t in range(num_teachers)] 
    
    #### Each cource assign to single teacher 
    for c in range(num_cources):
        model.Add(sum(x[t][c] for t in range(num_teachers))==1)
    #### cource will not asined to t if it not in specialization list 
    for t in range(num_teachers):
        for c in range(num_cources):
            if c+1 not in specialization[t]:
                model.Add(x[t][c]==0)

    #### handle conflict 
    for conflict in conflicts:
        c1 = conflict[0]
        c2 = conflict[1]
        for t in range(num_teachers):
            model.Add(x[t][c1-1] + x[t][c2-1]<=1)     

    max_cap = model.NewIntVar(0,num_cources,'max_cap')
    for t in range(num_teachers):
        model.Add(sum(x[t][c] for c in range(num_cources))<= max_cap)

    model.Minimize(max_cap)
    #### solve 
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    ## print result 
    if status == cp_model.OPTIMAL:
        return solver.Value(max_cap)
    else:
        return -1  # No feasible solution               
def main():
    num_teachers, num_cources, specialization, conficts = read_input()
    print(sovle_BCA(num_teachers, num_cources, specialization, conficts))
if __name__=="__main__":
    main()