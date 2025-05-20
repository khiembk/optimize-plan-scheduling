from ortools.sat.python import cp_model

def read_input():
    n = int(input())
    return n

def solve_sodoku_cp(n):
    model = cp_model.CpModel()
    
    x = [[model.NewIntVar(1,9, f'x{i}_{j}') for j in range(9)] for i in range(9)] 

    for i in range(9):
        
        model.add_all_different(x[i][j] for j in range(9))

    for i in range(9):
        model.add_all_different(x[j][i] for j in range(9))

    for pivot_x in range(0,9,3):
        for pivot_y in range(0,9,3):
             model.add_all_different(x[pivot_x + i][pivot_y + j] for j in range(3) for i in range(3))        
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for i in range(9):
            print(' '.join(str(solver.Value(x[i][j])) for j in range(9)))
    else:
        print("Solution not found")    
if __name__ =="__main__":
    n = read_input()
      
    solve_sodoku_cp(n)