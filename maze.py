from random import random, randint, randrange, choice
from numpy.random import shuffle
from heapq import heappush, heappop

class DisjointedSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1

def add_start_end(grid, width, height):
    if random() > 0.5: # Randomly choose whether entrance and exit are on the sides or top and bottom
        valid_start = [index for index, x in enumerate(grid[1]) if x == 0]
        valid_end = [index for index, x in enumerate(grid[height-2]) if x == 0]
        start, end = (0, choice(valid_start)), (height-1, choice(valid_end))
    else:
        valid_start = [index for index, y in enumerate([y[1] for y in grid]) if y == 0]
        valid_end = [index for index, y in enumerate([y[width-2] for y in grid]) if y == 0]
        start, end = (choice(valid_start), 0), (choice(valid_end), width-1)

    grid[start[0]][start[1]] = 0 # Add an entrance at the top
    grid[end[0]][end[1]] = 0 # Add an exit the bottom
    return start, end

def initialize_djs_and_grid(grid, width, height):
    cell_to_tree = {}
    tree_count = 0
    
    for row in range(1, height - 1, 2):
        for col in range(1, width - 1, 2):
            cell_to_tree[(row, col)] = tree_count
            tree_count += 1
            grid[row][col] = 0

    djs = DisjointedSet(tree_count)
    return cell_to_tree, tree_count, djs

def kruskals(width, height):
    width, height = width*2+1, height*2+1
    grid = [[1 for _ in range(width)] for _ in range(height)]
    cell_to_tree, tree_count, djs = initialize_djs_and_grid(grid, width, height)

    edges = []
    for row in range(2, height - 1, 2):
        for col in range(1, width - 1, 2):
            edges.append((row, col))
    for row in range(1, height - 1, 2):
        for col in range(2, width - 1, 2):
            edges.append((row, col))

    shuffle(edges)

    for row, col in edges:
        if row % 2 == 0:  # Vertical edge
            tree1 = cell_to_tree[(row - 1, col)]
            tree2 = cell_to_tree[(row + 1, col)]
        else:  # Horizontal edge
            tree1 = cell_to_tree[(row, col - 1)]
            tree2 = cell_to_tree[(row, col + 1)]

        if djs.find(tree1) != djs.find(tree2):
            djs.union(tree1, tree2)
            tree_count -= 1
            grid[row][col] = 0

        if tree_count == 1:
            break

    start, end = add_start_end(grid, width, height)
    return start, end, grid

def get_neighbors_generate(grid, node):
    neighbors = []
    for direction in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] == 1:
            neighbors.append(neighbor)
    return neighbors

def walk(grid, row, col):
    current_row, current_col = row, col
    unvisited_neighbors = get_neighbors_generate(grid, (current_row, current_col))
    while len(unvisited_neighbors) > 0:
        neighbor = choice(unvisited_neighbors)
        grid[neighbor[0]][neighbor[1]] = 0
        grid[(neighbor[0] + current_row) // 2][(neighbor[1] + current_col) // 2] = 0
        current_row, current_col = neighbor
        unvisited_neighbors = get_neighbors_generate(grid, (current_row, current_col))

def hunt(grid, width, height):
    for row in range(1, height, 2):
        for col in range(1, width, 2):
            if grid[row][col] == 0 and len(get_neighbors_generate(grid, (row, col))) > 0:
                return row, col
    return -1, -1
        
def hunt_and_kill(width, height):
    grid = [[1 for _ in range(width)] for _ in range(height)]    

    row, col = randrange(1, height, 2), randrange(1, width, 2)
    grid[row][col] = 0

    while row != -1 and col != -1:
        walk(grid, row, col)
        row, col = hunt(grid, width, height)
    
    start, end = add_start_end(grid, width, height)
    return start, end, grid

def recursive_backtracker(width, height):
    grid = [[1 for _ in range(width)] for _ in range(height)]

    row, col = randrange(1, height, 2), randrange(1, width, 2)
    track = [(row, col)]
    grid[row][col] = 0

    while track:
        row, col = track[-1]
        neighbors = get_neighbors_generate(grid, (row, col))

        if len(neighbors) == 0:
            track.pop()
        else:
            nrow, ncol = choice(neighbors)
            grid[nrow][ncol] = 0
            grid[(nrow + row) // 2][(ncol + col) // 2] = 0
            track += [(nrow, ncol)]

    start, end = add_start_end(grid, width, height)
    return start, end, grid

def ellers(width, height):
    grid = [[1 for _ in range(width)] for _ in range(height)]
    cell_to_tree, tree_count, djs = initialize_djs_and_grid(grid, width, height)

    for row in range(1, height-2, 2):        
        for col in range(1, width-2, 2):
            if random() > 0.5:
                tree1 = cell_to_tree[(row, col)]
                tree2 = cell_to_tree[(row, col+2)]
                if djs.find(tree1) != djs.find(tree2):
                    djs.union(tree1, tree2)
                    grid[row][col+1] = 0
    
        # Count the cells in each set
        unique_sets = []
        curr_set = []
        for col in range(1, width-2, 2):
            curr_set.append((row, col))
            tree1 = cell_to_tree[(row, col)]
            tree2 = cell_to_tree[(row, col+2)]
            if djs.find(tree1) == djs.find(tree2):
                if col+2 == width-2:
                    curr_set.append((row, col+2))
                    unique_sets.append(curr_set)
            else:
                unique_sets.append(curr_set)
                curr_set = []
                if col+2 == width-2:
                    unique_sets.append([(row, col+2)])
        
        for tree in unique_sets:
            vertical_connections = randint(1, len(tree))
            for _ in range(vertical_connections):
                row, col = choice(tree)
                tree1 = cell_to_tree[(row, col)] # Get the tree of the current cell and the tree of the point two rows down
                tree2 = cell_to_tree[(row+2, col)]
                djs.union(tree1, tree2)
                grid[row+1][col] = 0
                tree.remove((row, col))

    # Join all unconnected sets in the bottom row
    row = height-2
    for col in range(1, width-2, 2):
        tree1 = cell_to_tree[(row, col)]
        tree2 = cell_to_tree[(row, col+2)]
        if djs.find(tree1) != djs.find(tree2):
            djs.union(tree1, tree2)
            grid[row][col+1] = 0
    
    start, end = add_start_end(grid, width, height)
    return start, end, grid

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors_solve(grid, node):
    neighbors = []
    for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] == 0:
            neighbors.append(neighbor)
    return neighbors

def astar(maze, start, goal):
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            total_path = [current]
            while current in came_from:
                current = came_from[current]
                total_path.append(current)
            total_path.reverse()
            return total_path

        for neighbor in get_neighbors_solve(maze, current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [i[1] for i in open_set]:
                    heappush(open_set, (f_score[neighbor], neighbor))

    return None # No path found (should never happen with mazes generated by the implemented algorithms)
