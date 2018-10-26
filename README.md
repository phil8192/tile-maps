# Tile maps

> Mapping a set of random points to a uniform lattice

# Problem

Given a set of N polygons corresponding to countries/regions/municipalities find
a [regular tessellation](http://mathworld.wolfram.com/RegularTessellation.html)
of N triangles, squares, or hexagons where each tile corresponds to a country
such that the
[original spatial arrangement is preserved](http://blog.apps.npr.org/2015/05/11/hex-tile-maps.html)
as much as possible.

More generally, find a mapping from a set of N arbitrary/random points whilst
preserving the original arrangement.

The code in this repository is experimental.
For an excellent/stable R package solution to this problem, see
[Joseph Bailey](https://github.com/jbaileyh)'s
[geogrid](https://github.com/jbaileyh/geogrid).


# Integer Linear Programming (ILP) approach

My first approach to this problem makes use of Linear Programming.

## Installing COIN-OR

[Cbc](https://projects.coin-or.org/Cbc) (Coin-or branch and cut) is an
open-source mixed integer programming solver. It is faster than
the [GNU Linear Programming Kit](https://www.gnu.org/software/glpk/) (GLPK).

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


# Simulated Annealing (SA) approach

My second approach to this problem makes use of the popular Simulated Annealing
metaheuristic.



# References

* [Formulating Linear and Integer Linear Programs: A Rogues' Gallery](https://core.ac.uk/download/pdf/36730539.pdf)

* [Area Cartograms: Their Use and Creation](http://www.dannydorling.org/wp-content/files/dannydorling_publication_id1448.pdf) - Daniel Dorling. Appendix lists code for a circular force-directed/gravity method for cartogram generation. (see section 9 in book)

* [Let’s Tesselate: Hexagons For Tile Grid Maps](http://blog.apps.npr.org/2015/05/11/hex-tile-maps.html) - NPR visuals.

* [Integer Linear Programming Model approach)](https://kunigami.blog/category/computer-science/integer-programming/) - interesting formulation.

* [Area Cartograms: Their Use and Creation](http://www.dannydorling.org/wp-content/files/dannydorling_publication_id1448.pdf) - Daniel Dorling, 1996.

* [US as an hexagonal map](https://kunigami.blog/2016/11/04/us-as-an-hexagonal-map/) - Formalisation of problem as an Integer Programming Model.

* [Hexagonal Grids](http://www.redblobgames.com/grids/hexagons/) - Distances, path-finding and geometry.

* [Animated mapping is bringing elections to life](http://www.geog.ox.ac.uk/news/articles/150506-animated-mapping-elections.html)

* [ONS - Visualising your constituency](http://visual.ons.gov.uk/visualising-your-constituency/) - Geographic cartogram of UK.

* [Something About The Automated Stippling Drawing](http://community.wolfram.com/groups/-/m/t/759091) - Very interesting.

* [Conformal Projections](http://www.progonos.com/furuti/MapProj/Dither/ProjConf/projConf.html)

* [Conceptualisation of a D3 linked view with a hexagonal cartogram](http://www.ralphstraumann.ch/blog/2013/05/conceptualisation-of-a-d3-linked-view-with-hexagonal-cartogram/)

* [Crystallographic defect](https://en.wikipedia.org/wiki/Crystallographic_defect) - Clues from defective lattice? Perform Annealing?

* [Molecular dynamics](https://en.wikipedia.org/wiki/Molecular_dynamics)

* [Crystallisation](http://practicalmaintenance.net/?p=1085) -- Simulate

* [New metastable form of ice and its role in the homogeneous crystallisation of water](http://www.nature.com/nmat/journal/v13/n7/full/nmat3977.html)

* [Linear Assignment](https://github.com/src-d/lapjv) - mapping a set of size N to a a grid of size N. \*\*\*
