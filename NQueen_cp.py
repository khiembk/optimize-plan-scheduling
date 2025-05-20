from ortools.sat.python import cp_model

def read_input():
    n = int(input())
    return n


def solveNQueen(n):
    model = cp_model.CpModel()

    x = [model.NewIntVar(1,n,f'x_{i}') for i in range(n)]

    model.add_all_different(x)
    model.add_all_different(x[i] - i for i  in range(n))
    model.add_all_different(x[i] + i for i  in range(n))

    solver = cp_model.CpSolver()
    
    status  = solver.Solve(model)
    
    if status in (cp_model.OPTIMAL , cp_model.FEASIBLE):
        print(n)
        print(" ".join(str(solver.Value(x[i])) for i in range(n)))
    else:
        print("Solution not found")    
    

    return 0

if __name__ == "__main__":
    n = read_input()
    solveNQueen(n)