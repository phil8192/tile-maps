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
            if not c: continue
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


def acceptance_probability(current_state, new_state, temperature):
    """the probability of accepting a candidate state.

    1 if new_state - current_state > 0 (always accept an improvement.)

    [0,1] otherwise. according to: (new_state - current_state) / temperature.

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
    
    see https://en.wikipedia.org/wiki/Simulated_annealing#Acceptance_probabilities
    """
    d = new_state - current_state
    return 1 if d > 0 else math.exp(d / temperature)


conf = load_conf('geojson/counties.geojson', 'Name')
regions = conf['regions']
neighbours = conf['neighbours']

rows = 13
cols = 16 
#rows = 16 
#cols = 32

grid = random_grid(regions, rows, cols)
adj_matrix = adjacency_matrix(neighbours, regions)

last_max = max_score = eval_candidate(grid, adj_matrix)

t = 0.05
a = 0.9999999
#t=0.001
#a=1

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
    if t > 0.0001:
        t = t*a

    grid[i1][j1] = v2
    grid[i2][j2] = v1
        
    score = eval_candidate_mod(grid, adj_matrix)

    if score > max_score:
        last_max = max_score = score
        best_s = res_to_string(grid, regions)
        #subprocess.call('clear', shell=True) 
        #print(best_s)
        #print('heat = {:.6f} best = {}'.format(t, max_score))
    elif score > last_max or random.random() <= t:
        last_max = score
        if i % 100 == 0:
            subprocess.call('clear', shell=True)
            print(best_s)
            print(res_to_string(grid, regions))
            print('heat = {:.6f} best = {} current = {} '.format(t, max_score, score))
    else:
        grid[i2][j2] = v2 
        grid[i1][j1] = v1
 

