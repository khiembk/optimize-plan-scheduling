def input_inequation(file_path):    
    with open(file_path, "r") as f:
        # Read the first line containing m, n, p
        m, n = map(int, f.readline().split())

        # Read the list of m numbers
        c = list(map(int, f.readline().split()))

        # Read the n x m matrix
        matrix_inequation = [list(map(int, f.readline().split())) for _ in range(n)]
        b_inequation = list(map(int, f.readline().split()))

    return m, n, c, matrix_inequation, b_inequation

def read_input():
    # Read n and m
    n, m = map(int, input().split())

    # Read the list C of length n
    C = list(map(int, input().split()))

    # Read the matrix A of size m x n
    A = [list(map(int, input().split())) for _ in range(m)]

    # Read the list b of length m
    b = list(map(int, input().split()))

    return n, m, C, A, b

def convertToStandard(m,n, matrix_inequation, b_inequation):
    for index in range(m):
        cur_row = matrix_inequation[index]
        for j in range(m):
            cur_row.append(0)

        cur_row[n + index] = 1
        matrix_inequation[index] = cur_row
    
    return matrix_inequation, b_inequation
            
def InitLastRow(c, m,n):
    lastRow = (m+n)*[0]
    for i in range(n): 
        lastRow[i] = -c[i]

    return lastRow    

def find_min_negative_column_lr(lastRow):
    min_value = 0
    min_index = -1
    for index in range(lastRow):
        if (lastRow[index] < min_value):
                min_value = lastRow[index]
                min_index = index

    return min_index

def standardlize_row_with_index(cur_row, rhs, index):
    standard_value = cur_row[index]
    for i in range(len(cur_row)):
        cur_row[i] = cur_row[i]/standard_value

    rhs = rhs/standard_value

    return cur_row, rhs

def Calculate_estimate(matrix_euqation, index, rhs):
    estimation = []
    for i in range(len(matrix_equation)): 
        row = matrix_equation[i]
        if row[index] <= 0: 
            estimation.append(float('inf'))
        else: 
            estimation.append(rhs[i]/ row[index])    

    return estimation

def find_row_pivot(estimation):
    index = -1
    max_value = float('inf')
    for i in range(len(estimation)):
        if (estimation[i] < max_value):
            index = i
            max_value = estimation[i]

    return index

def linear_transform_row(cur_row, pivot_index, pivot_row, rsh, cur_row_index, rsh_pivot):
    scale_value = cur_row[pivot_index]
    rsh[cur_row_index] = rsh[cur_row_index] - scale_value*rsh_pivot
    for i in range(len(cur_row)):
        cur_row[i] = cur_row[i] - scale_value*pivot_row[i]

    return cur_row, rsh

def update_last_row(cur_lastrow, pivot_row, rsh_pivot, pivot_index):
    return 0    

if __name__ == "__main__":
    n, m, c, matrix_inequation, b_inequation = read_input()
    matrix_equation, b_equation = convertToStandard(m,n, matrix_inequation, b_inequation)
    #print(matrix_equation)
    lastRow = InitLastRow(c,m,n)
    cur_result = 0 


     
