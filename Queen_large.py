"""
Description
Find a solution to place n queens on a chess board such that no two queens attack each other.
A solution is represented by a sequence of variables: x[1], x[2], . . ., x[n] in which x[i] is the row of the queen on column i (i = 1, . . ., n)

Input
Line 1: contains a positive integer n (10 <= n <= 10000)

Output
Line 1: write n 
Line 2: write x[1], x[2],  . . ., x[n] (after each value is a SPACE character)
"""
from ortools.sat.python import cp_model

def read_input():
   n = int(input())
   return n


def main():
   n = read_input() 
   model = cp_model.CpModel()
    
   x = [model.NewIntVar(1, n , f"x_{i}") for i in range(n)]

   ########
   model.add_all_different(x)   
   model.add_all_different([x[i] + i for i in range(n)])
   model.add_all_different([x[i] + i for i in range(n)])
   solver = cp_model.CpSolver()
   solver.parameters.enumerate_all_solutions = False 
   status = solver.Solve(model)
   if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
      print(n)
      print(" ".join(str(solver.Value(x[i])) for i in range(n)))
   else:
        print("No solution found.")

if __name__ == "__main__": 
   main()