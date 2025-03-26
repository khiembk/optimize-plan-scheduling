import random
from ortools.sat.python import cp_model

def solve_by_cp(n):
    """Solves N-Queens using Constraint Programming for small n (n <= 100)."""
    model = cp_model.CpModel()
    
    x = [model.NewIntVar(1, n, f"x_{i}") for i in range(n)]

    # Constraints: No two queens attack each other
    model.add_all_different(x)   
    model.add_all_different([x[i] + i for i in range(n)])
    model.add_all_different([x[i] - i for i in range(n)])

    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = False 
    status = solver.Solve(model)

    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print(n)
        print(" ".join(str(solver.Value(x[i])) for i in range(n)))
    else:
        print("No solution found.")

def min_conflicts(n, max_steps=1000):
    """Solves the N-Queens problem using the Min-Conflicts heuristic for large n (n > 100)."""
    # Step 1: Initial greedy assignment
    queens = list(range(1, n+1))  # 1-based indexing
    random.shuffle(queens)

    def count_conflicts():
        """Counts conflicts in current board state."""
        row_counts = {}
        diag1_counts = {}
        diag2_counts = {}
        conflicts = 0

        for col, row in enumerate(queens):
            d1 = row - col
            d2 = row + col
            conflicts += row_counts.get(row, 0) + diag1_counts.get(d1, 0) + diag2_counts.get(d2, 0)

            row_counts[row] = row_counts.get(row, 0) + 1
            diag1_counts[d1] = diag1_counts.get(d1, 0) + 1
            diag2_counts[d2] = diag2_counts.get(d2, 0) + 1

        return conflicts

    for i in range(max_steps):
        if count_conflicts() == 0 or i == max_steps-1:
            return queens  # Solution found

        # Step 2: Identify a conflicting column
        col = random.randint(0, n-1)

        # Step 3: Find a row that minimizes conflicts
        best_row = queens[col]
        min_conflicts = float("inf")

        for row in range(1, n+1):
            queens[col] = row
            conflicts = count_conflicts()
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_row = row

        # Step 4: Update queen position
        queens[col] = best_row

    return None  # No solution found within the given steps

def solve_by_heuristic(n):
    solution = min_conflicts(n)
    #print(" ".join(map(str, solution)))
    if solution:
        print(n)
        print(" ".join(map(str, solution)))
    else:
        print("No solution found.")

def main():
    n = int(input()) 
    if n <= 100:
        solve_by_cp(n)
    else: 
        solve_by_heuristic(n)

if __name__ == "__main__":
    main()
