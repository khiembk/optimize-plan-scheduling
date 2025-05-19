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

def solve_segment_cp(queens, start, end):
    """Solves a segment of the N-Queens problem exactly using CP."""
    n = end - start
    if n <= 0:
        return True  # Empty segment is trivially solved
    
    model = cp_model.CpModel()
    x = [model.NewIntVar(1, len(queens), f"x_{i}") for i in range(n)]  # Use full board size for row domain
    
    # Constraints within the segment
    model.AddAllDifferent(x)
    model.AddAllDifferent([x[i] + (start + i) for i in range(n)])  # Diagonal +
    model.AddAllDifferent([x[i] - (start + i) for i in range(n)])  # Diagonal -

    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = False
    status = solver.Solve(model)

    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        for i in range(n):
            queens[start + i] = solver.Value(x[i])
        return True
    return False

def count_inter_segment_conflicts(queens, seg1_start, seg1_end, seg2_start, seg2_end):
    """Counts diagonal conflicts between two segments."""
    conflicts = 0
    for col1 in range(seg1_start, seg1_end):
        row1 = queens[col1]
        for col2 in range(seg2_start, seg2_end):
            row2 = queens[col2]
            if abs(row1 - row2) == abs(col1 - col2):  # Diagonal conflict
                conflicts += 1
    return conflicts

def get_most_conflicted_queen(queens, n1, n2):
    """Identifies the queen with the most conflicts in the range n1 to n2."""
    cur_queen = queens[n1:n2]
    row_counts = {}
    diag1_counts = {}
    diag2_counts = {}
    conflicts_per_queen = [0] * len(cur_queen)

    for col, row in enumerate(cur_queen, start=n1):
        d1 = row - col
        d2 = row + col
        conflicts_per_queen[col - n1] += (
            row_counts.get(row, 0) +
            diag1_counts.get(d1, 0) +
            diag2_counts.get(d2, 0)
        )
        row_counts[row] = row_counts.get(row, 0) + 1
        diag1_counts[d1] = diag1_counts.get(d1, 0) + 1
        diag2_counts[d2] = diag2_counts.get(d2, 0) + 1

    for col in range(len(cur_queen) - 1, -1, -1):
        row = cur_queen[col]
        true_col = col + n1
        d1 = row - true_col
        d2 = row + true_col
        row_counts[row] -= 1
        diag1_counts[d1] -= 1
        diag2_counts[d2] -= 1
        conflicts_per_queen[col] += (
            row_counts.get(row, 0) +
            diag1_counts.get(d1, 0) +
            diag2_counts.get(d2, 0)
        )

    max_conflicts = -1
    max_col = n1
    for col, conflicts in enumerate(conflicts_per_queen):
        if conflicts > max_conflicts:
            max_conflicts = conflicts
            max_col = col + n1

    return max_col, max_conflicts

def solve_by_segmented_cp(n, segment_size=20):
    """Solves N-Queens by segmenting into exact CP solutions and resolving inter-segment conflicts."""
    queens = list(range(1, n + 1))
    random.shuffle(queens)
    
    # Step 1: Solve each segment exactly
    segments = [(i, min(i + segment_size, n)) for i in range(0, n, segment_size)]
    for start, end in segments:
        if not solve_segment_cp(queens, start, end):
            print("No solution found for segment", start, "to", end)
            return None

    # Step 2: Resolve inter-segment conflicts
    max_steps = 100  # Limit iterations for inter-segment fixing
    for index in range(max_steps):
        total_conflicts = 0
        conflict_found = False
        
        # Check conflicts between adjacent segments
        for i in range(len(segments) - 1):
            seg1_start, seg1_end = segments[i]
            seg2_start, seg2_end = segments[i + 1]
            conflicts = count_inter_segment_conflicts(queens, seg1_start, seg1_end, seg2_start, seg2_end)
            total_conflicts += conflicts
            if conflicts > 0:
                conflict_found = True
                # Fix the most conflicted queen in the combined range
                combined_start = seg1_start
                combined_end = seg2_end
                col, _ = get_most_conflicted_queen(queens, combined_start, combined_end)
                
                # Try moving this queen to minimize conflicts
                min_conflicts = float("inf")
                best_row = queens[col]
                for row in range(1, n + 1):
                    queens[col] = row
                    new_conflicts = count_inter_segment_conflicts(queens, seg1_start, seg1_end, seg2_start, seg2_end)
                    if new_conflicts < min_conflicts:
                        min_conflicts = new_conflicts
                        best_row = row
                queens[col] = best_row
        
        if not conflict_found or index == max_steps-1:
            print(n)
            print(" ".join(map(str, queens)))
            return queens
    
    print("No solution found after resolving inter-segment conflicts.")
    return None

def main():
    n = int(input())
    if n <= 100:
        solve_by_cp(n)  # Use original CP solver for small n
    else:
        solve_by_segmented_cp(n, segment_size=20)  # Use segmented approach for larger n

if __name__ == "__main__":
    main()