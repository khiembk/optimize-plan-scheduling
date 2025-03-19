"""
Perform the domain consistency for the CSP with n variables X1, X2, . . ., Xn with a set of LEQ constraints under the form: Xi <= Xj + D

Input
Line 1: contains a positive integer n (1 <= n <= 50)
Line i+1 (i = 1, 2, ..., n): contains a positive integer k and k subsequent integers v(i,1), v(i,2), . . ., v(i,k) which are the values of the domain of Xi 
Line n+2: contains a positive integer m (1 <=  m <= 50) which is the number of LEQ constraints
Line n+2+i (i = 1, 2, ..., m): contains i, j and D which represent the LEQ constraint Xi <= Xj + D
 
Output
Line i (i = 1, 2, ..., n): contains q (number of values of the domain of Xi) and a sequence (increasing order) of values of the domain of Xi the DC propagation (after each value, there is a SPACE character) or print FAIL if the domain of some variable becomes empty.

"""
from collections import deque

def propagate_constraint(i, j, D, domains, constraints_to_check):
    # Prune domains based on Xi <= Xj + D
    domain_i = domains[i]
    domain_j = domains[j]
    changed = False

    # Prune Xi: Xi <= max(Xj) + D
    max_j_plus_D = max(domain_j) + D
    new_domain_i = [x for x in domain_i if x <= max_j_plus_D]
    if new_domain_i != domain_i:
        domains[i] = new_domain_i
        changed = True

    # Prune Xj: Xj >= min(Xi) - D
    if domain_i:  # Only if Xi still has values
        min_i_minus_D = min(domain_i) - D
        new_domain_j = [x for x in domain_j if x >= min_i_minus_D]
        if new_domain_j != domain_j:
            domains[j] = new_domain_j
            changed = True

    return changed

def enforce_domain_consistency(n, domains, constraints):
    # Queue for constraints to process (AC-3 algorithm)
    queue = deque(constraints)
    while queue:
        i, j, D = queue.popleft()
        if propagate_constraint(i, j, D, domains, queue):
            # If domains changed, recheck all constraints involving i or j
            for c in constraints:
                if c[0] == i or c[1] == i or c[0] == j or c[1] == j:
                    if c not in queue:  # Avoid duplicates
                        queue.append(c)
        
        # Check for empty domains
        if not domains[i] or not domains[j]:
            return False
    return True

def main():
    # Read input
    n = int(input())
    
    # Read domains for each variable Xi
    domains = []
    for _ in range(n):
        line = list(map(int, input().split()))
        k = line[0]
        domain = sorted(line[1:k+1])  # Ensure increasing order
        domains.append(domain)
    
    # Read constraints
    m = int(input())
    constraints = []
    for _ in range(m):
        i, j, D = map(int, input().split())
        constraints.append((i-1, j-1, D))  # Convert to 0-based indexing
    
    # Enforce domain consistency
    success = enforce_domain_consistency(n, domains, constraints)
    
    # Output result
    if not success:
        print("FAIL")
    else:
        for i in range(n):
            domain = domains[i]
            print(f"{len(domain)} {' '.join(map(str, domain))}")

if __name__ == "__main__":
    main()