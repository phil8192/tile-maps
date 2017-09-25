import random
import itertools
from read import load_conf


def random_grid(regions, rows, cols):
    grid = [[None]*rows for i in range(0, cols)]
    avail = list(itertools.product(range(0, rows), range(0, cols)))
    random.shuffle(avail)
    for k in range(0, len(regions)):
        i, j = avail.pop()
        grid[i][j] = k
    return grid


def adjacency_matrix(neighbour_tuples, regions):
    grid = [[False]*len(regions) for i in range(0, len(regions))]
    for i, j in neighbour_tuples:
        grid[i][j] = True
        #grid[j][i] = True
    return grid 
    

def eval_candidate(grid, adj):
    score = 0
    row_len = len(grid)
    col_len = len(grid[0])
    for i in range(0, row_len):
        row = grid[i]
        for j in range(0, col_len):
           centre = row[j] 
           if centre:
               if i > 0:
                   north = grid[i - 1][j]
                   if north and adj[centre][north]:
                       score += 1
               if j < col_len - 1:
                   east = grid[i][j + 1]
                   if east and adj[centre][east]:
                       score += 1
               if i < row_len - 1:
                   south = grid[i + 1][j]
                   if south and adj[centre][south]:
                       score += 1
               if j > 0:
                   west = grid[i][j - 1]
                   if west and adj[centre][west]:
                       score += 1
    return score


conf = load_conf('geojson/counties.geojson', 'Name')
regions = conf['regions']
neighbours = conf['neighbours']
rows = cols = 10

grid = random_grid(regions, rows, cols)
adj_matrix = adjacency_matrix(neighbours, regions)

score = eval_candidate(grid, adj_matrix)

print(grid)
print(adj_matrix)
print(score)
