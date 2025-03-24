import random

def read_input():
    n = int(input().strip())
    distance = [list(map(int, input().split())) for _ in range(n)]
    return n, distance

def compute_cost(path, distance):
    n = len(path)
    cur_cost = 0
    
    for i in range(n - 1):
        cur_cost += distance[path[i]][path[i + 1]]
    
    cur_cost += distance[path[-1]][path[0]]
    return cur_cost

def random_permute(path, num_for, cur_cost, distance):
    min_cost = cur_cost
    optimal_path = path[:]
    
    for _ in range(num_for):
        cur_path = path[:] 
        a, b = random.sample(range(len(path)), 2)
        cur_path[a], cur_path[b] = cur_path[b], cur_path[a]  
        
        i_cost = compute_cost(cur_path, distance)
        if i_cost <= min_cost:
            optimal_path = cur_path[:]
            min_cost = i_cost

    return optimal_path, min_cost  

def heuristic(init_path, n, distance, num_step=100):
    path = [x - 1 for x in init_path]  
    
    
    cur_cost = compute_cost(path, distance)
    
    
    for _ in range(num_step):
        
        path, cur_cost = random_permute(path, num_for=100, cur_cost=cur_cost, distance=distance)
        
    
    return cur_cost, [x + 1 for x in path]  
def main():
    n, distance = read_input()
    num_random = 100
    init_path = list(range(1, n + 1))
    c_path = [x - 1 for x in init_path]  # Ensure proper 1-based indexing
    min_cost = compute_cost(c_path,distance)
    best_path = init_path
    for _ in range(num_random):
        temp_path = init_path[:]  # Copy init_path before shuffling
        random.shuffle(temp_path)
        # print("temp_path: ",temp_path)
        cur_cost, cur_best_path = heuristic(temp_path, n, distance, num_step=50)
        if (cur_cost <= min_cost):
            min_cost = cur_cost
            best_path = cur_best_path
    print(n)  
    print(*best_path)  

if __name__ == "__main__":
    main()
