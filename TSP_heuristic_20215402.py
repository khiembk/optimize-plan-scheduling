#PYTHON 
import random
from itertools import permutations
def read_input():
    
    n = int(input().strip())
    distance = [list(map(int, input().split())) for _ in range(n)]
    return n, distance


def tsp_backtracking(n, distance):
    
    min_cost = float('inf')
    best_path = []

    def backtrack(cur_path, cur_cost, visited):
        nonlocal min_cost, best_path

        
        if len(cur_path) == n:
            total_cost = cur_cost + distance[cur_path[-1]][cur_path[0]] 
            if total_cost < min_cost:
                min_cost = total_cost
                best_path = cur_path[:]
            return
        
       
        for next_city in range(n):
            if next_city not in visited:
                next_cost = cur_cost + distance[cur_path[-1]][next_city]

               
                if next_cost >= min_cost:
                    continue
                
               
                visited.add(next_city)
                cur_path.append(next_city)
                backtrack(cur_path, next_cost, visited)
                visited.remove(next_city)
                cur_path.pop()
    
    
    for start_city in range(n):
        backtrack([start_city], 0, {start_city})
    
    return min_cost, [x + 1 for x in best_path]




def nearest_neighbor(n, distance,start_point):
    
    unvisited = set(range(n))  
    path = [start_point]  
    cur_city = start_point
    unvisited.remove(start_point)
    total_cost = 0

    while unvisited:
        next_city = min(unvisited, key=lambda city: distance[cur_city][city])  # Find nearest
        total_cost += distance[cur_city][next_city]  
        path.append(next_city)
        unvisited.remove(next_city)
        cur_city = next_city

   
    total_cost += distance[cur_city][start_point]
    path.append(start_point)  
    
    return total_cost, [x + 1 for x in path]


def main():
    n, distance = read_input()
    min_cost = float('inf')
    best_path = []
    if n <= 18:
        cost, best_path = tsp_backtracking(n, distance)
    else:
        for _ in range(30):
           start_point  = random.randint(0, n - 1)
           cost, path = nearest_neighbor(n, distance, start_point)
           if cost < min_cost:
               min_cost = cost
               best_path = path[:]

    print(n)
    print(*best_path)

if __name__ == "__main__":
    main()
