def read_input():
    n, m = map(int, input().split())
    C = list(map(int, input().split()))
    A = [list(map(int, input().split())) for _ in range(m)]
    b = list(map(int, input().split()))
    return n, m, C, A, b

def convertToStandard(m, n, matrix_inequation, b_inequation):
    for index in range(m):
        cur_row = matrix_inequation[index]
        for j in range(m):
            cur_row.append(1 if j == index else 0)  # Slack variables
    return matrix_inequation, b_inequation

def InitLastRow(c, m, n):
    lastRow = [0] * (m + n)
    for i in range(n):
        lastRow[i] = -c[i]  # Negative for maximization
    return lastRow

def find_min_negative_column_lr(lastRow):
    min_value = 0
    min_index = -1
    for index in range(len(lastRow)):
        if lastRow[index] < min_value:
            min_value = lastRow[index]
            min_index = index
    return min_index

def standardize_row_with_index(cur_row, rhs, index):
    standard_value = cur_row[index]
    if standard_value == 0:
        raise ValueError("Pivot element cannot be zero")
    for i in range(len(cur_row)):
        cur_row[i] = cur_row[i] / standard_value
    rhs = rhs / standard_value
    return cur_row, rhs

def calculate_estimate(matrix_equation, index, rhs):
    estimation = []
    for i in range(len(matrix_equation)):
        row = matrix_equation[i]
        if row[index] <= 0:
            estimation.append(float('inf'))
        else:
            estimation.append(rhs[i] / row[index])
    return estimation

def find_row_pivot(estimation):
    index = -1
    min_value = float('inf')
    for i in range(len(estimation)):
        if 0 < estimation[i] < min_value:
            index = i
            min_value = estimation[i]
    return index

def linear_transform_row(cur_row, pivot_index, pivot_row, rhs, cur_row_index, rhs_pivot):
    scale_value = cur_row[pivot_index]
    rhs[cur_row_index] = rhs[cur_row_index] - scale_value * rhs_pivot
    for i in range(len(cur_row)):
        cur_row[i] = cur_row[i] - scale_value * pivot_row[i]
    return cur_row, rhs

def update_last_row(cur_lastrow, pivot_row, rhs_pivot, pivot_index):
    scale_value = cur_lastrow[pivot_index]
    for i in range(len(cur_lastrow)):
        cur_lastrow[i] = cur_lastrow[i] - scale_value * pivot_row[i]
    return cur_lastrow

def simplex_method(n, m, c, matrix_equation, b_equation):
    lastRow = InitLastRow(c, m, n)
    while True:
        pivot_col = find_min_negative_column_lr(lastRow)
        if pivot_col == -1:  # Optimal solution found
            break

        estimation = calculate_estimate(matrix_equation, pivot_col, b_equation)
        pivot_row_idx = find_row_pivot(estimation)
        if pivot_row_idx == -1:  # Unbounded
            return None

        matrix_equation[pivot_row_idx], b_equation[pivot_row_idx] = standardize_row_with_index(
            matrix_equation[pivot_row_idx], b_equation[pivot_row_idx], pivot_col
        )

        for i in range(m):
            if i != pivot_row_idx:
                matrix_equation[i], b_equation = linear_transform_row(
                    matrix_equation[i], pivot_col, matrix_equation[pivot_row_idx],
                    b_equation, i, b_equation[pivot_row_idx]
                )

        lastRow = update_last_row(lastRow, matrix_equation[pivot_row_idx], b_equation[pivot_row_idx], pivot_col)

    # Extract solution
    solution = [0] * n
    for j in range(n):
        col = [matrix_equation[i][j] for i in range(m)]
        if col.count(1) == 1 and col.count(0) == m - 1:  # Basic variable
            row_idx = col.index(1)
            solution[j] = b_equation[row_idx]
    
    return solution

if __name__ == "__main__":
    n, m, c, matrix_inequation, b_inequation = read_input()
    matrix_equation, b_equation = convertToStandard(m, n, matrix_inequation, b_inequation)
    
    solution = simplex_method(n, m, c, matrix_equation, b_equation)
    if solution is None:
        print("UNBOUNDED")
    else:
        print(n)
        print(" ".join(map(str, solution)))