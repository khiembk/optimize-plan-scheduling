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
    for index in range(n):
        cur_row = matrix_inequation[index]
        for j in range(n):
            cur_row.append(0)

        cur_row[m + index] = 1
        matrix_inequation[index] = cur_row
    
    return matrix_inequation
            
    
if __name__ == "__main__":
    m, n, c, matrix_inequation, b_inequation = read_input()
    matrix_equation = convertToStandard(m,n, matrix_inequation, b_inequation)
    print(matrix_equation)

     
