# use pulp - a python abstraction layer for linear programming modeling. 
from pulp import *

regions = 4

# neighbours (diagonal of neighbourhood list)
# (decision variables). N_0_2 = region 0 and 2 are neighbours.
neighbours = {
    (0, 1): LpVariable(cat=LpBinary, name='N_0_1'),
    (0, 2): LpVariable(cat=LpBinary, name='N_0_2'),
    (1, 2): LpVariable(cat=LpBinary, name='N_1_2'),
    (1, 3): LpVariable(cat=LpBinary, name='N_1_3')
}

# maximise... (maybe later want to minimise or penalise non-assignments..
model = LpProblem('tiles', LpMaximize)
model += lpSum(neighbours.values())

# subject to...

# all possible assignments for regions to cells in a 3x3 matrix.
# ASS_0_1_5 (ASS_row_col_region) means: "cell in row 0, col 1 contains region
# 5." or "region 5 assigned to cell 0, col 1". the number of cell assignment
# variables will then be rows*cols*regions.
rows, cols = (3, 3)
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
        model += r1_N <= r1_cell, "REL_R1_{}_{}_{}_{}".format(r1, r2, row, col)
        model += r1_N <= lpSum(r2_cell_neighbours), "REL_R2_{}_{}_{}_{}".format(r1, r2, row, col)
        possible.append(r1_N)
    # from all of the possible N_r1_r2_row_col centre and surrounding neighbour possibilities,
    # if there exists an assignment where r2 surrounds r1, then N_r1_r2 will be true (since we
    # are trying to maximise N_r1_r2 in the objective function...
    model += v <= lpSum(possible), "REL_N_{}_{}".format(r1, r2)

# output the model in CPLEX LP format. (for verification/debugging)
# note that this can be solved with GNU Linear Programming Kit) for example,
# by doing:
# 
# glpsol --lp tiles.lp
model.writeLP('tiles.lp')

# do it!
model.solve()

print("status:", LpStatus[model.status])

# show result.
for _, ass in cell_assignments.items():
    if value(ass) == 1:
       print(ass) 

