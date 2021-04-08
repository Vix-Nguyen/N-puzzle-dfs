import sys
import grid
import solver


# validate command line input
if len(sys.argv) != 2:
    sys.stderr.write(
        'Error: must be 2 command line arguments of the form:\npython driver.py <board>\n')
    sys.exit()

# convert input string to a list of ints
input_list = sys.argv[1].split(',')
input_list = list(map(int, input_list))
print(input_list)

if len(input_list) not in [4, 9, 16, 25]:
    sys.stderr.write(
        "Error: input grid must be nxn square where n is 2, 3, 4 or 5\n")
    sys.exit()

ordered_list = sorted(input_list)
for index, number in enumerate(ordered_list):
    if number != index:
        sys.stderr.write(
            "Error: input list must contain all numbers from 0 to n^2 - 1\n")
        sys.exit()


try:
    solver = solver.Solver(input_list)
except ValueError:
    print('no solution exists')
    sys.exit()


solution_metrics = solver.depth_first_search()

print("path_to_goal: " + str(solution_metrics.path_to_goal))
print("cost_of_path: " + str(solution_metrics.cost_of_path()))
print("nodes_expanded: " + str(solution_metrics.nodes_expanded))
print("fringe_size: " + str(solution_metrics.fringe_size()))
print("max_fringe_size: " + str(solution_metrics.max_fringe_size))
print("search_depth: " + str(solution_metrics.search_depth))
print("max_search_depth: " + str(solution_metrics.max_search_depth))
print("running_time: " + str(solution_metrics.search_time) + "ms")
