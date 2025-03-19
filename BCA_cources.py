from ortools.sat.python import cp_model

def solve_balanced_course_assignment(N, P, credits, alpha, beta, lamda, gamma, L):
    model = cp_model.CpModel()

   
    x = [[model.NewBoolVar(f'x[{j},{i}]') for i in range(N)] for j in range(P)]

    
    for j in range(P):
        model.Add(sum(x[j][i] * credits[i] for i in range(N)) >= lamda)  
        model.Add(sum(x[j][i] * credits[i] for i in range(N)) <= gamma)  
        model.Add(sum(x[j][i] for i in range(N)) >= alpha)  
        model.Add(sum(x[j][i] for i in range(N)) <= beta)   
   
    for i in range(N):
        model.Add(sum(x[j][i] for j in range(P)) == 1)

    
    for constaint in L:
        i, j = constaint[0], constaint[1]
        for q in range(P):
            for p in range(q + 1):  
                model.Add(x[q][i] + x[p][j] <= 1)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Print results
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for j in range(P):
            print(f"Semester {j}: ", end="")
            for i in range(N):
                if solver.Value(x[j][i]) == 1:
                    print(f"[Course {i}, Credit {credits[i]}]", end=" ")
            print()
    else:
        print("No feasible solution found.")
   
def read_input():
    num_sub, num_term = map(int, input().split())
    cur_credits = list(map(int, input().split()))
    L = [[1,2],[3,4],[7,9]]
    min_sub = int(input())
    max_sub = int(input())
    min_credit = int(input())
    max_credit = int(input())
    return num_sub,num_term, cur_credits,L,min_sub,max_sub, min_credit, max_credit

def main():
    num_sub,num_term, cur_credits,L,min_sub,max_sub, min_credit, max_credit = read_input()
    solve_balanced_course_assignment(num_sub,num_term,cur_credits,min_sub,max_sub,min_credit, max_credit,L)
if __name__=="__main__":
    main()