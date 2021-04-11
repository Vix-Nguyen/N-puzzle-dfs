import grid
import custom_structures
import copy
import math
import metric


class Solver:

    """Controller class."""

    def __init__(self, input_list):
        """Initialise Solver object. Raise ValueError if solution not possible."""

        if not self.solvable(input_list):
            raise ValueError('A solution is not possible')

        # don't just bind to input state. we want the object to have its OWN state
        # https://docs.python.org/2/library/copy.html
        self.initial_state = copy.deepcopy(self.list_to_grid(input_list))
        print('Init state: ', self.initial_state)

        self.goal_state = self.set_goal_state(input_list)
        print('Goal state: ', self.goal_state)

        # using custom structures so we can implement a custom __contains__()
        self.frontier = custom_structures.Frontier()
        self.explored = custom_structures.Explored()

        self.metrics = metric.Metric(self.frontier)

    def depth_first_search(self):
        """Explore search space using depth-first search"""

        self.metrics.start_timer()

        initial_grid = grid.Grid(self.initial_state)

        # push the initial node
        self.frontier.queue.append(initial_grid)

        # while queue is not empty..
        while self.frontier.queue:

            # get the node by at the right-end of Frontier
            state = self.frontier.queue.pop()
            # print('---cur state : ', state.state)
            state.visualize_grid()

            self.metrics.search_depth = len(state.path_history)
            self.metrics.update_max_depth()

            # add the the checked node to right-end of Explored
            self.explored.set.add(state)

            # if the game end (matched with goal state):
            #   print time and depth of the tree and queue
            if self.goal_test(state):
                self.metrics.path_to_goal = state.path_history
                self.metrics.stop_timer()
                return self.metrics

            # put child node of current node to Frotier
            self.expand_nodes(state)

        # if we get to here it's must be something wrong
        raise ValueError('Shouldn\'t have got to here - gone tits')

    def expand_nodes(self, starting_grid):
        """Take a grid state, add all possible 'next moves' to the frontier"""

        node_order = ['up', 'down', 'left', 'right']
        # THIS ACTUALLY TAKE RIGHT - LEFT - UP - DOWN in order
        # So to clear the understanding, we reverse it

        node_order = reversed(node_order)
        # NOW IT TAKE UP - DOWN - LEFT - RIGHT

        # we treat node as the tile have position (right left down up) compare to the blank tile
        for node in node_order:

            # get the next grid if folow the move
            next_grid = grid.Grid(starting_grid.state)

            if next_grid.move(node):  # returns false if move not possible

                # pass path history from previous grid to the next grid
                # using copy(soft) to avoid python's reference bindings
                next_grid.path_history = copy.copy(starting_grid.path_history)

                next_grid.path_history.append(node)

                # check if next grid is a completely new state
                if next_grid not in self.frontier and next_grid not in self.explored:

                    # put the next grid at the right-end of the Frontier
                    self.frontier.queue.append(next_grid)

                    self.metrics.update_max_fringe()

            # Count all the nodes (even it's a blank node)
            self.metrics.nodes_expanded += 1

    def goal_test(self, current):
        """Compare a given current state to the goal state. Return Boolean"""

        if current.state == self.goal_state:
            return True
        else:
            return False

    def set_goal_state(self, input_list):
        """Construct and return a grid state in the correct order."""

        # initialise empty grid state
        n = int(math.sqrt(len(input_list)))
        goal_state = [['-' for x in range(n)] for y in range(n)]

        # populate goal grid with ordered tiles
        i = 0
        j = 0
        count = 1

        # Goal state with blank at bottom right tile:
        #1, 2, ...
        # ....
        # ...., 0
        while i < n:
            if count == n * n:
                count = 0
            goal_state[i][j] = count
            count += 1
            j += 1
            if j == n:
                j = 0
                i += 1

        return goal_state

    def solvable(self, input_list):
        """Determine if a given input grid is solvable.

        It turns out that a lot of grids are unsolvable.
        http://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable/838818
        https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
        https://en.wikipedia.org/wiki/15_puzzle#Solvability

        This implementation assumes blank tile goal position is bottom right.
        """

        # solvability depends on the width...
        width = int(math.sqrt(len(input_list)))

        # ..whether the row that zero is on is odd/even...
        temp_grid = grid.Grid(self.list_to_grid(input_list))

        zero_location = temp_grid.locate_tile(0, temp_grid.state)

        if zero_location[0] % 2 == 0:
            zero_odd = False
        else:
            zero_odd = True

        # .. and the number of 'inversions' (not counting '0')

        # strip the blank tile
        input_list = [number for number in input_list if number != 0]

        inversion_count = 0
        list_length = len(input_list)

        for index, value in enumerate(input_list):
            for value_to_compare in input_list[index + 1: list_length]:
                if value > value_to_compare:
                    inversion_count += 1

        if inversion_count % 2 == 0:
            inversions_even = True
        else:
            inversions_even = False

        if width % 2 == 0:
            width_even = True
        else:
            width_even = False

        # see https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
        return ((not width_even and inversions_even)
                or
                (width_even and (zero_odd == inversions_even)))

    def list_to_grid(self, tile_list):
        """Take a list of length n^2, return a nxn 2D list"""

        n = int(math.sqrt(len(tile_list)))

        # initialise empty grid
        input_grid = [['-' for x in range(n)] for y in range(n)]
        # populate grid with tiles
        i = 0
        j = 0
        for tile in tile_list:
            input_grid[i][j] = tile
            j += 1
            if j == n:
                j = 0
                i += 1

        return input_grid
