# Tile maps

> Map a set of random points to a uniform lattice

# Problem

Given a set of N polygons corresponding to countries/regions/municipalities find 
a [regular tessellation](http://mathworld.wolfram.com/RegularTessellation.html) of N triangles, squares, 
or hexagons where each tile corresponds to a country such that the [original spatial arrangement is
preserved](http://blog.apps.npr.org/2015/05/11/hex-tile-maps.html) as much as possible.

More generally, find a mapping from a set of N arbitrary/random points whilst preserving the original 
arrangement as much as possible.

## Integer linear programming approach

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

### Example run (Newport)

26 of 44 possible neighbourhood relations satisfied.

```
Result - Stopped on time limit

Objective value:                26.00000000
Lower bound:                    44.000
Gap:                            -0.41
Enumerated nodes:               3676
Total iterations:               17364320
Time (CPU seconds):             14421.75
Time (Wallclock seconds):       2015.19

Option for printingOptions changed from normal to all
Total time (CPU seconds):       14421.77   (Wallclock seconds):       2015.23

status: Not Solved

-----------------------------------------
| ST | PI |    | RO | AL |    |    |    |
-----------------------------------------
| GA | TR |    | BE | SH |    |    |    |
-----------------------------------------
| GR | MA | LI | BE | ST | VI |    |    |
-----------------------------------------
|    |    | AL | CA | MA |    |    |    |
-----------------------------------------
|    | LL | RI | LA |    |    |    |    |
-----------------------------------------
|    |    |    | LL |    |    |    |    |
-----------------------------------------
|    |    |    |    |    |    |    |    |
-----------------------------------------
|    |    |    |    |    |    |    |    |
-----------------------------------------

GR = Graig
RO = Rogerstone
BE = Bettws
MA = Malpas
SH = Shaftesbury
CA = Caerleon
LA = Langstone
AL = Allt-yr-yn
ST = St Julians
BE = Beechwood
AL = Alway
RI = Ringland
LL = Llanwern
GA = Gaer
ST = StowHill
VI = Victoria
TR = Tredegar Park
MA = Marshfield
LI = Liswerry
LL = Llanwern
PI = Pillgwenlly
```

## Refs

[Formulating Linear and Integer Linear Programs: A Rogues' Gallery](https://core.ac.uk/download/pdf/36730539.pdf)


# Dependencies

## Python

```
pip3 install pulp
```

## Installing COIN-OR

Cbc (Coin-or branch and cut) is an open-source mixed integer programming solver.
It is faster than the GLPK.

```
git clone --branch=stable/2.9 https://github.com/coin-or/Cbc Cbc-2.9
cd Cbc-2.9
git clone --branch=stable/0.8 https://github.com/coin-or-tools/BuildTools/
chmod 0700 BuildTools/get.dependencies.sh
BuildTools/get.dependencies.sh fetch
./configure --prefix=/usr/local --enable-cbc-parallel
make
sudo make install
```

verify parallel enabled

```
cbc -threads 8 -unitTest -dirMiplib=_MIPLIB3DIR_ -miplib
```



## References

[Area Cartograms: Their Use and Creation](http://www.dannydorling.org/wp-content/files/dannydorling_publication_id1448.pdf) - Daniel Dorling. Appendix lists code for a circular force-directed/gravity method for cartogram generation. (see section 9 in book)

[Let’s Tesselate: Hexagons For Tile Grid Maps](http://blog.apps.npr.org/2015/05/11/hex-tile-maps.html) - NPR visuals.

[Integer Linear Programming Model approach)](https://kunigami.blog/category/computer-science/integer-programming/) - interesting formulation.

[Area Cartograms: Their Use and Creation](http://www.dannydorling.org/wp-content/files/dannydorling_publication_id1448.pdf) - Daniel Dorling, 1996.

[US as an hexagonal map](https://kunigami.blog/2016/11/04/us-as-an-hexagonal-map/) - Formalisaton of problem as an Integer Programming Model.

[Hexagonal Grids](http://www.redblobgames.com/grids/hexagons/) - Distances, path-finding and geometry.

[Animated mapping is bringing elections to life](http://www.geog.ox.ac.uk/news/articles/150506-animated-mapping-elections.html)

[ONS - Visualising your constituency](http://visual.ons.gov.uk/visualising-your-constituency/) - Geographic cartogram of UK.

[Something About The Automated Stippling Drawing](http://community.wolfram.com/groups/-/m/t/759091) - Very interesting.

[Conformal Projections](http://www.progonos.com/furuti/MapProj/Dither/ProjConf/projConf.html)

[Conceptualisation of a D3 linked view with a hexagonal cartogram](http://www.ralphstraumann.ch/blog/2013/05/conceptualisation-of-a-d3-linked-view-with-hexagonal-cartogram/)

[Crystallographic defect](https://en.wikipedia.org/wiki/Crystallographic_defect) - Clues from defective lattice? Perform Annealing?

[Molecular dynamics](https://en.wikipedia.org/wiki/Molecular_dynamics)

[Crystallisation](http://practicalmaintenance.net/?p=1085) -- Simulate

[New metastable form of ice and its role in the homogeneous crystallization of water](http://www.nature.com/nmat/journal/v13/n7/full/nmat3977.html)

[Linear Assignment](https://github.com/src-d/lapjv) - mapping a set of size N to a a grid of size N. \*\*\*
