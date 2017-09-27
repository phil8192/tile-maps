import math
import random
import itertools
import subprocess
from read import load_conf


def random_grid(regions, rows, cols):
    grid = [[None]*cols for i in range(0, rows)]
    avail = list(itertools.product(range(0, rows), range(0, cols)))
    random.shuffle(avail)
    for k in range(0, len(regions)):
        i, j = avail.pop()
        grid[i][j] = k
    return grid


def adjacency_matrix(neighbour_tuples, regions):
    grid = [[0]*len(regions) for i in range(0, len(regions))]
    for i, j in neighbour_tuples:
        grid[i][j] = 1
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
                   if north:
                       score += adj[centre][north]
               if j < col_len - 1:
                   east = grid[i][j + 1]
                   if east:
                       score += adj[centre][east] 
               if i < row_len - 1:
                   south = grid[i + 1][j]
                   if south:
                       score += adj[centre][south]
               if j > 0:
                   west = grid[i][j - 1]
                   if west:
                       score += adj[centre][west]
    return score


def eval_candidate_mod(grid, adj):
    score = 0
    row_len = len(grid)
    col_len = len(grid[0])
    for i in range(0, row_len):
        row = grid[i]
        for j in range(0, col_len):
            c = row[j]
            if c is None: continue
            n = grid[(i - 1) % row_len][j]
            e = grid[i][(j + 1) % col_len]
            s = grid[(i + 1) % row_len][j]
            w = grid[i][(j - 1) % col_len]
            if n: score += adj[c][n]
            if e: score += adj[c][e]
            if s: score += adj[c][s]
            if w: score += adj[c][w]
    return score
 

def res_to_string(grid, regions):
    res = []
    rows = len(grid)
    cols = len(grid[0])
    rs = []
    for i in range(0, rows):
        for j in range(0, cols):
            ass = grid[i][j]
            if ass is None:
                ass_region = '   '
            else:
                ass_region = regions[ass]['s_name']    
            rs.append('| {} '.format(ass_region))
        rs.append('|')
        rs = ''.join(rs)
        res.append('-' * len(rs))
        res.append('\n')
        res.append(rs)
        res.append('\n')
        rs = []
    res.append('-' * len(rs))
    res.append('\n')
    return ''.join(res)


def acceptance_probability(old_score, new_score, temperature=1):
    """the probability of accepting a candidate state.

    1 if new_score - old_score > 0 (always accept an improvement.)

    [0,1] otherwise. according to: (new_score - old_score) / temperature.

    this means that with a fixed temperature (say 1000), less damaging moves are
    (exponentially) favoured over really bad moves:

    p = [ exp(0), exp(-inf) ) ..
    e.g.,
    exp(-1) ~= 0.368 > exp(-5) ~= 0.0067
    
    note that moves resulting in a < -5 loss in objective score are highly
    unlikely: this can be scaled..

    initially, with maximum temperature, we allow for disruptive moves, although
    still favour least disruptive. 

    as the temperature decreases over time, according to some cooling schedule,
    we want to further still inhibit disruptive moves.
    e.g.,
    exp(-1 / 10) ~= 0.9 > exp(-1 / 1)  ~= 0.36

    without temperature, %prob. of selecting bad move = 

    >>> ['{:.2f}'.format(100*math.exp(-x)) for x in range(1, 9)]
    ['36.79', '13.53', '4.98', '1.83', '0.67', '0.25', '0.09', '0.03']  

    -1 = no change in score. (sometimes accept sideways moves)
    -2 = -1 change.. 

    see:
    https://en.wikipedia.org/wiki/Simulated_annealing#Acceptance_probabilities
    """
    d = new_score - old_score - 1
    return 1 if d >= 0 else math.exp(d / temperature)


conf = load_conf('geojson/counties.geojson', 'Name')
regions = conf['regions']
neighbours = conf['neighbours']

rows = 13
cols = 16 
#rows = 16 
#cols = 32

grid = random_grid(regions, rows, cols)
adj_matrix = adjacency_matrix(neighbours, regions)

#import sys
#import pprint
#pprint.pprint(conf)
#print(adj_matrix)
#sys.exit(0)

old_score = best_score = eval_candidate(grid, adj_matrix)

# highest possible score.
max_score = len(neighbours) 

# highest change (-+) in score possible from a single move (swaps)
# can use this later to scale acceptance probability function. 
max_move_score = 8


#t = 0.05
#a = 0.9999999


# ['{:.9f}'.format(100*math.exp(-x/1)) for x in range(1, 9)]
# ['36.787944117', '13.533528324', '4.978706837', '1.831563889', '0.673794700', '0.247875218', '0.091188197', '0.033546263']
t = 1

# cooling schedule
a = 0.9999999

# ['{:.9f}'.format(100*math.exp(-x/0.25)) for x in range(1, 9)]
# ['1.831563889', '0.033546263', '0.000614421', '0.000011254', '0.000000206', '0.000000004', '0.000000000', '0.000000000']
min_temp = 0.25

print_every = 100
best_s = ''
i = 0
while True:

    i1 = random.randint(0, rows - 1)
    j1 = random.randint(0, cols - 1)
    i2 = random.randint(0, rows - 1)
    j2 = random.randint(0, cols - 1)

    v1 = grid[i1][j1]
    v2 = grid[i2][j2]

    # dont swap empty positions...    
    if not (v1 or v1): continue

    i = i+1
    if t > min_temp: t = t*a

    grid[i1][j1] = v2
    grid[i2][j2] = v1
        
    new_score = eval_candidate_mod(grid, adj_matrix)

    if acceptance_probability(old_score, new_score, t) >= random.random():
        # accept the candidate move
        old_score = new_score
        if new_score > best_score:
            # new maxima found
            best_score = new_score
            best_s = res_to_string(grid, regions)
        else:
            # exploring
            if i % print_every == 0:
                subprocess.call('clear', shell=True)
                print(best_s)
                print(res_to_string(grid, regions))
                print('temperature = {:.6f} best = {} current = {} '.format(t, best_score, new_score))
    else:
        # reject the candidate move
        grid[i1][j1] = v1
        grid[i2][j2] = v2
   
