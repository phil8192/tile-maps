# Hexmap integer linear programming

Try to solve hexmap problem using IP.

This is the test case:

```
      from this... (regions of crete)


                                     XXXXXXXXXXXXX
                         XXXXXXXXXXXXX         XXX                                                               XX
                      XXXX                   XXX                                                              XXXXXX
                 XXXXXX                     XX                                                              XXX   XX
               XXX                           XX                                                           XX   XXXX
               XXX                          XX                                                          XXX  XXX
                 XX                         XXXX                                                      XXX   XX
                 X                            X                                                     XXX     XX
                XX                           XX                                  XXXX             XXX        X
              XXX                           XX                                XXXX  XXXXXXX     XXX          XX
           XXXX X               0           X                               XXX          X   XXXX             X
      XXXXXX    XXXX  XXXXX                 X                             XXX            XXXXX                 XXXXXX
     XX  X         XXX    XX                X                   XXXXXXXXXXX                                         X
    XX                 XXXXX                X                  XX                                                 XX
    XX               XX                     XX               XXX                                              XXXXX
     XXX    2       XX                       XXXX        XXXXXX                                              XX
       XX          XX                           XX      XX    X                          3                  X
       X         XXXXXXX   XXX                  XXXX  XXX     XXXX        XX                                X
        X      XXX     XXXX  XXXX               X  XXX           XXXXXXXXX XXXX                            XX
        XXXX  XX                XXXXXX          X                              XX                         XX
            XXX                       XX   XXXXXX                               X                        XX
              XXX                      XXXXX                                     XXXXXX                 XX
                X                                        1                            X               XXX
                XXX                                                                  XX            XXXX
                  XX                                                  XXXXXXXXXXXXX  XX        XXXXX
                   X        XXXXXXXX                        XXXXXXXXXXX            XXXXXXXXXXXX
                   X   XXXX       XXXXXXXXXXXXXXXXXXXXXXXXXX
                    XXXXX


      ...to this
        

                             +-----------+
                             |     |     |
                             |  2  |  0  |
                             |     |     |
                             +-----------------+
                                   |     |     |
                                   |  1  |  3  |
                                   |     |     |
                                   +-----------+
```

## Running

Generate model. Output in CPLEX LP format:

```
python3 ./model.py
```

Now feed it to an IP solver. Default is GNU Linear Programming Kit.
COIN-OR will be faster. Gurobi (propriatory will be fastest).

```
glpsol --lp tiles.lp
```

### Example run

Expect that 3 neighbourhood relations can be satisfied.

```
GLPSOL: GLPK LP/MIP Solver, v4.63
Parameter(s) specified in the command line:
 --lp tiles.lp
Reading problem data from 'tiles.lp'...
89 rows, 76 columns, 316 non-zeros
76 integer variables, all of which are binary
183 lines were read
GLPK Integer Optimizer, v4.63
89 rows, 76 columns, 316 non-zeros
76 integer variables, all of which are binary
Preprocessing...
40 hidden covering inequaliti(es) were detected
89 rows, 76 columns, 316 non-zeros
76 integer variables, all of which are binary
Scaling...
 A: min|aij| =  1.000e+00  max|aij| =  1.000e+00  ratio =  1.000e+00
Problem data seem to be well scaled
Constructing initial basis...
Size of triangular part is 89
Solving LP relaxation...
GLPK Simplex Optimizer, v4.63
89 rows, 76 columns, 316 non-zeros
      0: obj =  -0.000000000e+00 inf =   3.000e+00 (1)
      7: obj =  -0.000000000e+00 inf =   0.000e+00 (0)
*    56: obj =   4.000000000e+00 inf =   1.110e-16 (0)
OPTIMAL LP SOLUTION FOUND
Integer optimization begins...
+    56: mip =     not found yet <=              +inf        (1; 0)
+    71: >>>>>   3.000000000e+00 <=   4.000000000e+00  33.3% (4; 0)
+   281: mip =   3.000000000e+00 <=     tree is empty   0.0% (0; 37)
INTEGER OPTIMAL SOLUTION FOUND
Time used:   0.0 secs
Memory used: 0.2 Mb (219016 bytes)
```
