import sys
import grid
import solver


input_list = [1, 7, 2, 9, 4, 0, 12, 3, 14, 5, 6, 17,
              8, 19, 10, 11, 22, 13, 24, 15, 16, 21, 18, 23, 20]

""" Uncomment these line to get input by keyboard (user define)"""
# # validate command line input
# if len(sys.argv) != 2:
#     sys.stderr.write(
#         'Error: must be 2 command line arguments of the form:\npython driver.py <board>\n')
#     sys.exit()

# # convert input string to a list of ints
# input_list = sys.argv[1].split(',')
# input_list = list(map(int, input_list))
print(input_list)


def checkSquareNum(n):

    for i in range(1, n + 1):
        if (i**2 == n):
            return True

    return False


# We actually can solve with any NxN, but i sometimes want to limit it
if not checkSquareNum(len(input_list)):
    sys.stderr.write(
        "Error: input grid must be nxn square\n")
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

print("Goal path: " + str(solution_metrics.path_to_goal))
print("Cost of path: " + str(solution_metrics.cost_of_path()))
print("Total node expanded: " + str(solution_metrics.nodes_expanded))
print("Frontier size: " + str(solution_metrics.fringe_size()))
print("Max Frontier get: " + str(solution_metrics.max_fringe_size))
print("Goal state depth: " + str(solution_metrics.search_depth))
print("Max depth get: " + str(solution_metrics.max_search_depth))
print("Running time: " + str(solution_metrics.search_time) + "ms")
