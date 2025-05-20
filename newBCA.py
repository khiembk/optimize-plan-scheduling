from ortools.linear_solver import pywraplp

def read_intput():
   line = list(map(int, input().split()))
   t = line[0]
   c = line[1]
   spec = []
   for i in range(t):
      line = list(map(int, input().split()))
      newline = [ele - 1 for ele in line]
      spec.append(newline[1:])

   num_conf = int(input())
   conflics = []
   for _ in range(num_conf):
      line = list(map(int, input().split()))
      newline = [ele - 1 for ele in line]
      conflics.append(newline)

     
   return t,c, spec, conflics

def solve_bca(t, c, spec, conflics):
   solver = pywraplp.Solver.CreateSolver('SCIP')
   x = [[solver.BoolVar(f'x_{i}_{j}') for j in range(c)] for i in range(t)]
   
   for i in range(t):
      for j in range(c):
         if j not in spec[i]:
            solver.Add(x[i][j] == 0)

   for j in range(c):
      solver.Add(sum(x[i][j] for i in range(t)) == 1)

   for cur_conflics in conflics:
      c1 = cur_conflics[0]
      c2 = cur_conflics[1]
      for i in range(t):
         solver.Add(x[i][c1] + x[i][c2] <=1)    

   Max_load = solver.IntVar(0,c,'Max_load')
   for i in range(t):
      solver.Add(sum(x[i][j] for j in range(c))<=Max_load)

   solver.Minimize(Max_load)

   status = solver.Solve()

   if status == pywraplp.Solver.OPTIMAL:
      print(int(Max_load.solution_value()))               
   else:
      print("-1")
   return 0

if __name__ =="__main__":
   t,c , spec, conflics = read_intput()
   solve_bca(t,c,spec, conflics)