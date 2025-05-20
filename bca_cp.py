# Có N môn học 1, 2, …, N cần được phân bổ vào P học kỳ 1, 2, …, P
# • Mỗi môn học i có số tín chỉ là credit(i)
# • L = {(i, j)}: tập các cặp môn học (i, j) trong điều kiện tiên quyết (môn i phải được xếp và học kỳ trước học
# kỳ của môn j)
# • Cho trước các hằng số , , , . Hãy tìm cách xếp N môn học vào P học kỳ sao cho
# • Tổng số môn học trong mỗi học kỳ phải lớn hơn hoặc bằng  và nhỏ hơn hoặc bằng 
# • Tổng số tín chỉ các môn học trong mỗi học kỳ phải lớn hơn hoặc bằng  và nhỏ hơn hoặc bằng 

from ortools.sat.python import cp_model

def read_input():
    line  = list(map(int, input().split()))
    cources = line[0]
    terms = line[1]
    credits = list(map(int, input().split()))
    conflics = []
    k = int(input())
    for _ in range(k):
        line = list(map(int, input().split()))
        conflics.append(line)

    return cources, terms, credits, conflics

def solve_bca_cp(max_cources, min_cources, max_credits, min_credits, cources, terms, credits, conflics):
    model = cp_model.CpModel()

    x = [[model.NewBoolVar(f'x_{i}_{j}') for j in range(terms)] for i in range(cources)]

    for j in range(cources):
        model.Add(sum(x[j][i] for i in range(terms)) ==1)

    for j in range(terms):
        model.Add(sum(x[i][j] for i in range(cources)) <= max_cources)
        model.Add(sum(x[i][j] for i in range(cources)) >= min_cources)
        model.Add(sum(x[i][j]*credits[i] for i in range(cources)) <= max_credits)
        model.Add(sum(x[i][j]*credits[i] for i in range(cources)) >= min_credits)
    
    for conflic in conflics:
        pre_c = conflic[0]-1
        pos_c = conflic[1]-1
        for i in range(terms):
            model.Add(sum(x[pre_c][j] for j in range(i))  >= x[pos_c][i])

    solver = cp_model.CpSolver()

    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for i in range(cources):
            print(f"course {i+1} :")
            for j in range(terms):
                if (solver.Value(x[i][j]) >0.5):
                    print(f"term : {j+1}")
                    break
    else:
        print("solution not found")        

    return 0

if __name__ == "__main__":
    cources, terms, credits, conflics = read_input()
    max_cources = 100
    min_cources = 1
    max_credits = 100
    min_credits = 1
    solve_bca_cp(max_cources,min_cources,max_credits, min_credits,cources,terms, credits, conflics)
