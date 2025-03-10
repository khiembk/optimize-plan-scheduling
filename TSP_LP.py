from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # Distance matrix (symmetric, 5 cities)
    data['distance_matrix'] = [
        [0, 10, 15, 20, 25],  # City 0
        [10, 0, 35, 25, 30],  # City 1
        [15, 35, 0, 30, 20],  # City 2
        [20, 25, 30, 0, 15],  # City 3
        [25, 30, 20, 15, 0],  # City 4
    ]
    data['num_vehicles'] = 1  # Single vehicle (salesman)
    data['depot'] = 0         # Starting point (City 0)
    return data

def print_solution(manager, routing, solution):
    """Prints the solution on console."""
    print(f'Objective: {solution.ObjectiveValue()} units')
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f' {manager.IndexToNode(index)} ->'
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f' {manager.IndexToNode(index)}\n'
    plan_output += f'Distance of the route: {route_distance} units\n'
    print(plan_output)

def main():
    """Solve the TSP."""
    # Instantiate the data problem
    data = create_data_model()

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot']
    )

    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc (distance between nodes)
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic (cheapest arc)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution
    if solution:
        print_solution(manager, routing, solution)
    else:
        print('No solution found!')

if __name__ == '__main__':
    main()