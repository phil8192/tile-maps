import copy
import math
import random
import itertools
import subprocess
import ascii_graph
import termcolor

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
        grid[j][i] = 1
    return grid 
    

def eval_candidate_mod(grid, adj):
    score = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            score += eval_position(grid, adj, i, j)
    return score


def eval_position(grid, adj, i, j):
    score = 0
    c = grid[i][j]
    if c is not None:
        row_len = len(grid)
        col_len = len(grid[0])
        n = grid[(i - 1) % row_len][j]
        e = grid[i][(j + 1) % col_len]
        s = grid[(i + 1) % row_len][j]
        w = grid[i][(j - 1) % col_len]
        if n is not None: score += adj[c][n]
        if e is not None: score += adj[c][e]
        if s is not None: score += adj[c][s]
        if w is not None: score += adj[c][w]
    return score


def res_to_string(grid, regions, fg='white', bg='on_blue', fill='on_blue'):
    res = []
    rows = len(grid)
    cols = len(grid[0])
    rs = []
    for i in range(0, rows):
        for j in range(0, cols):
            ass = grid[i][j]
            if ass is None:
                #rs.append('    ')
                rs.append(' ')
                rs.append(termcolor.colored('   ', fg, fill))
            else:
                rs.append(' ')
                rs.append(termcolor.colored(regions[ass]['s_name'], fg, bg, attrs=['bold']))
        #rs.append(' ')
        rs = ''.join(rs)
        #res.append(' ' * len(rs))
        res.append('\n')
        res.append(rs)
        res.append('\n')
        rs = []
    #res.append(' ' * len(rs))
    #res.append('\n')
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


import cProfile
pr = cProfile.Profile()
pr.enable()

conf = load_conf('geojson/counties.geojson', 'Name')
#conf = load_conf('geojson/us.geojson', 'NAME')
#conf = load_conf('geojson/constituencies.geojson', 'pcon16nm')

regions = conf['regions']
neighbours = conf['neighbours']

rows = 13
cols = 16 
#rows = 27 
#cols = 45

grid = random_grid(regions, rows, cols)
adj_matrix = adjacency_matrix(neighbours, regions)

#import sys
#import pprint
#pprint.pprint(conf)
#print(adj_matrix)
#sys.exit(0)

old_score = best_score = eval_candidate_mod(grid, adj_matrix)

# highest possible score.
max_score = len(neighbours) 

#t = 0.05
#a = 0.9999999

# ['{:.9f}'.format(100*math.exp(-x/1)) for x in range(1, 9)]
# ['36.787944117', '13.533528324', '4.978706837', '1.831563889', '0.673794700', '0.247875218', '0.091188197', '0.033546263']
t = 0.6

# cooling schedule
a = 0.999999999

# ['{:.9f}'.format(100*math.exp(-x/0.3)) for x in range(1, 9)]
# ['3.567399335', '0.127263380', '0.004539993', '0.000161960', '0.000005778', '0.000000206', '0.000000007', '0.000000000']
min_temp = 0.3

# stash best result for final output + restarts.
best_grid = None
restarts = 0
restart_limit = 20 

print_every = 100
best_s = ''
i = 0
#while 1:
for _ in range(0, 10000000): 
    # check if we should restart
    # https://en.wikipedia.org/wiki/Simulated_annealing#Restarts
    if best_score - old_score > restart_limit:
        # we have deviated too far from a good solution..
        grid = copy.deepcopy(best_grid)
        old_score = best_score
        restarts += 1
        # and also restart the cooling schedule?


    i1 = random.randint(0, rows - 1)
    j1 = random.randint(0, cols - 1)
    i2 = random.randint(0, rows - 1)
    j2 = random.randint(0, cols - 1)

    new_score = old_score

    v1 = grid[i1][j1]
    v2 = grid[i2][j2]
    new_score -= eval_position(grid, adj_matrix, i1, j1)
    new_score -= eval_position(grid, adj_matrix, i2, j2)

    # dont swap empty positions...    
    if v1 is None and v1 is None:
        continue

    i = i+1
    if t > min_temp: t = t*a

    grid[i1][j1] = v2
    grid[i2][j2] = v1
    new_score += eval_position(grid, adj_matrix, i1, j1)
    new_score += eval_position(grid, adj_matrix, i2, j2)

    if acceptance_probability(old_score, new_score, t) >= random.random():
        # accept the candidate move
        old_score = new_score
        if new_score > best_score:
            # new maxima found
            best_score = new_score
            best_s = res_to_string(grid, regions, 'white', 'on_blue', 'on_grey')
            best_grid = copy.deepcopy(grid)
        else:
            # exploring
            if i % print_every == 0:
                subprocess.call('clear', shell=True)
                print(best_s)
                print(res_to_string(grid, regions, 'cyan', 'on_grey', 'on_grey'))
                print('temperature = {:.6f} state restarts = {}'.format(t, restarts))
                graph_data = [('best result', best_score), ('current result', new_score)]
                for g in ascii_graph.Pyasciigraph(force_max_value=max_score).graph(data=graph_data):
                    print(g)
                
    else:
        # reject the candidate move
        grid[i1][j1] = v1
        grid[i2][j2] = v2
   


pr.disable()
pr.print_stats(sort='time')
