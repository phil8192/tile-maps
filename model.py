# use pulp - a python abstraction layer for linear programming modeling. 
import multiprocessing
from pulp import *

# crete
#conf = {
#    'regions': [ { 'name': 'aa' },
#                 { 'name': 'bb' },
#                 { 'name': 'cc' },
#                 { 'name': 'dd' } ],
#    # diagonal of neighbourhood list
#    'neighbours': [ (0, 1), (0, 2), (1, 2), (1, 3) ]
#}

# newport
conf = {
    'regions': [ { 'name': 'Graig' },        # 0
                 { 'name': 'Rogerstone' },   # 1
                 { 'name': 'Bettws' },       # 2
                 { 'name': 'Malpas' },       # 3
                 { 'name': 'Shaftesbury' },  # 4
                 { 'name': 'Caerleon' },     # 5
                 { 'name': 'Langstone' },    # 6
                 { 'name': 'Allt-yr-yn' },   # 7
                 { 'name': 'St Julians' },   # 8
                 { 'name': 'Beechwood' },    # 9
                 { 'name': 'Alway' },        # 10
                 { 'name': 'Ringland' },     # 11
                 { 'name': 'Llanwern' },     # 12
                 { 'name': 'Gaer' },         # 13
                 { 'name': 'StowHill' },     # 14
                 { 'name': 'Victoria' },     # 15
                 { 'name': 'Tredegar Park'}, # 16
                 { 'name': 'Marshfield' },   # 17
                 { 'name': 'Liswerry' },     # 18
                 { 'name': 'Llanwern' },     # 19
                 { 'name': 'Pillgwenlly' } ],# 20
    'neighbours': [ (0, 1), (0, 17), (0, 13), (17, 13), (17, 16), (17, 20), (17, 18), (1, 7), (1, 13), (1, 2), (7, 2), (7, 4), (7, 14), (13, 14), (13, 16), (16, 20), (2, 3), (2, 4), (3, 5),
(3, 8), (3, 4), (4, 8), (4, 14), (14, 20), (14, 15), (20, 18), (8, 5), (8, 9), (8, 15), (15, 9), (15, 18), (9, 5), (9, 10), (9, 18), (10, 5), (10, 11), (10, 18), (11, 5), (11, 6), (11, 12),
(11, 18), (5, 6), (18, 12), (19, 6) ] 
}

regions = len(conf['regions'])
# (decision variables). N_0_2 = region 0 and 2 are neighbours.
neighbours = {k: LpVariable(cat=LpBinary, name='N_{}_{}'.format(*k)) for k in conf['neighbours']}


# maximise... (maybe later want to minimise or penalise non-assignments..
model = LpProblem('tiles', LpMaximize)
model += lpSum(neighbours.values())

# subject to...

# all possible assignments for regions to cells matrix.
rows = cols = 7 #regions # worst case: all stacked on top of each other.. 
keys = itertools.product(range(0, rows), range(0, cols), range(0, regions))
cell_assignments = {k: LpVariable(cat=LpBinary, name='ASS_{}_{}_{}'.format(*k)) for k in keys}
#for _, ass in cell_assignments.items():
#    model += ass

# pack constraint: a cell can contain *at most* 1 region,
# ...for each cell:
for row, col in itertools.product(range(0, rows), range(0, cols)):
    possible_assignments = [cell_assignments[(row, col, region)] for region in range(0, regions)]
    at_most_one = lpSum(possible_assignments) <= 1
    model += at_most_one, 'PACK_{}_{}'.format(row, col)

# partition constraint: a region *must* be assigned to 1 cell.
for region in range(0, regions):
    possible_assignments = [cell_assignments[(row, col, region)] for row, col in itertools.product(range(0, rows), range(0, cols))]
    only_one = lpSum(possible_assignments) == 1
    model += only_one, 'PARTITION_{}'.format(region)

# link objective function decision variables with constraints.
for k, v in neighbours.items():
    r1, r2 = k # r1 <-> r2 neighbours
    possible = []
    # for each cell
    for row, col in itertools.product(range(0, rows), range(0, cols)):
        # ASS_row_col for r1 neighbour (centre)
        r1_cell = cell_assignments[(row, col, r1)]
        # .. and the (max) 4 N,E,S,W possible r2 neighbours
        r2_cell_neighbours = []
        N = (row-1, col, r2)
        E = (row, col+1, r2)
        S = (row+1, col, r2)
        W = (row, col-1, r2)
        if N in cell_assignments: # no N in 1st row
            r2_cell_neighbours.append(cell_assignments[N])
        if E in cell_assignments: # no E on last col
            r2_cell_neighbours.append(cell_assignments[E])
        if S in cell_assignments: # no S on last row
            r2_cell_neighbours.append(cell_assignments[S])
        if W in cell_assignments: # no W on first col
            r2_cell_neighbours.append(cell_assignments[W])
        r1_N = LpVariable(cat=LpBinary, name='N_{}_{}_{}_{}'.format(r1, r2, row, col))
        # N_r1_r2_row_col is true iff r1_cell is assigned and r2 is one of the neighbours.
        model += r1_N <= r1_cell, 'REL_R1_{}_{}_{}_{}'.format(r1, r2, row, col)
        model += r1_N <= lpSum(r2_cell_neighbours), 'REL_R2_{}_{}_{}_{}'.format(r1, r2, row, col)
        possible.append(r1_N)
    # from all of the possible N_r1_r2_row_col centre and surrounding neighbour possibilities,
    # if there exists an assignment where r2 surrounds r1, then N_r1_r2 will be true (since we
    # are trying to maximise N_r1_r2 in the objective function...
    model += v <= lpSum(possible), 'REL_N_{}_{}'.format(r1, r2)

# output the model in CPLEX LP format. (for verification/debugging)
# note that this can be solved with GNU Linear Programming Kit) for example,
# by doing:
# 
# glpsol --lp tiles.lp
model.writeLP('tiles.lp')

# using coin-or solver
threads = multiprocessing.cpu_count()
model.solve(solver=COIN_CMD(msg=True, mip=True, presolve=True, maxSeconds=1800*threads, threads=threads))
# using glpk solver
#model.solve()

print('status:', LpStatus[model.status])

# show result.
print()
rs = []
for row in range(0, rows):
    rs = []
    for col in range(0, cols):
        ass_region = '  '
        #rs.append("| {} ".format(row))
        for region in range(0, regions):
            if value(cell_assignments[(row, col, region)]) == 1:
                ass_region = conf['regions'][region]['name'][:2].upper()
                break
        rs.append('| {} '.format(ass_region))
    rs.append('|')
    rs = ''.join(rs)
    print('-' * len(rs))
    print(rs)
print('-' * len(rs))
print()

for region in conf['regions']:
    print('{} = {}'.format(region['name'][:2].upper(), region['name']))
