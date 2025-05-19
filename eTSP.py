from ortools.linear_solver import pywraplp

def tsp_with_precedence_mtz(n, d, Q):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        raise RuntimeError("SCIP solver not available.")

    # Decision variables: x[i][j] = 1 if go from i to j
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = solver.BoolVar(f'x_{i}_{j}')

    # Order variables: u[i] is the position in the tour
    u = {}
    for i in range(1, n):  # u[0] is the start node
        u[i] = solver.IntVar(1, n - 1, f'u_{i}')

    # Objective: minimize total distance
    solver.Minimize(solver.Sum(d[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j))

    # Each node must be entered and left exactly once
    for i in range(n):
        solver.Add(solver.Sum(x[i, j] for j in range(n) if i != j) == 1)
        solver.Add(solver.Sum(x[j, i] for j in range(n) if i != j) == 1)

    # MTZ constraints to eliminate subtours
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                solver.Add(u[i] - u[j] + (n - 1) * x[i, j] <= n - 2)

    # Precedence constraints: u[i] + 1 <= u[j] for (i, j) in Q
    for i, j in Q:
        if i != 0 and j != 0:
            solver.Add(u[i] + 1 <= u[j])

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Total distance:", solver.Objective().Value())

        # Step 1: Extract all tour edges
        edges = {(i, j) for (i, j) in x if x[i, j].solution_value() > 0.5}

        # Step 2: Reconstruct full path from edges
        path = [0]
        current = 0
        while len(path) < n:
            for (u, v) in edges:
                if u == current:
                    path.append(v)
                    current = v
                    break

        # Step 3: Return to start to complete cycle
        path.append(0)

        print("Path:", path)  # e.g. [0, 2, 3, 4, 1, 0]
        return path

    else:
        print("No optimal solution found.")
        return None

def read_input():
    n  =  int(input())
    distance = []
    for _ in range(n):
        line = list(map(int, input().split()))
        distance.append(line)
    
    q = int(input())
    constrains = []
    for _ in range(q):
        line = list(map(int, input().split()))
        constrains.append(line)

    return n, distance, q, constrains
    
if __name__ == "__main__":
   n, distance, q, constrains = read_input()
   tsp_with_precedence_mtz(n,distance,constrains)