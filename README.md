# Applied Topology Visualizations

The applied topology visualiation (ApTViz) package contains functions designed to create data graphics from common TDA analyses and structures. Visualization functions rely on some combination of [Plotly](https://plotly.com/python/), JavaScript, [Flask](https://flask.palletsprojects.com/en/1.1.x/), and [D3](https://observablehq.com/@d3).


<!-- Ann insert nice picture here -->

Contact [me](https://www.aesizemore.com/) for questions and comments.

----
## Table of Contents

* Expected data organization
* Assumptions
* Filtered simplicial complex visualizations
* Subset-focused visualizations
* PH output viz
* More on html output files
* Future goals

## Data organization

These functions are currently very opinionated on the organization of data. 

`fsc_df` is a [pandas data frame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with one row per simplex and the following columns:

**Required**
* `cell_id`: An integer used to reference the simplex. This number should be unique to the simplex.
* `dim`: An integer *k* denoting the dimension of the $k$-simplex.
* `nodes`: A list of integers denoting the nodes involved in the simplex.
* `faces`: A list of cell ids indicating the faces of the simplex.

**Semi-required**
* `weight`: Float designating simplex weight. See Assumptions section for more information. This column can be ignored if only using the rank of simplices. See function flags for rank vs. weight.
* `rank`: An integer indicating the simplex rank. See [1, 2] for more details. This column can be ignored if only using the weight of simplices. See function flags for rank vs. weight.

**Optional**
* "indicator column": Entries = 0, 1. Examples include `is_maximal`, in which maximal simplices are marked with 1, and `in_subcomplex`, in which simplices involved in a particular subcomplex are marked with 1.


`bar_df` 


## Assumptions

These functions are particular about data organization (see previous section), but they also make a few assumptions about the data.

1. *Simplex weights are positive.* Most of the code should work regardless, but at this time the functions have not been designed to handle negative weights, specifically.

2. *Simplex weights are ranked highest to lowest.* Following common edge-weighting schemes in the neuroscience and biology, we assume that the highest-weighted simplices are the strongest in the complex.

3. *Simplex weights are unique.* Most functions should work regardless, but currently the code is not designed to handle non-unique weights. This will be removed in a later version.

4. *Simplex ranks are unique.* Most functions should work regardless, but currently the code is not designed to handle non-unique ranks. This will be removed in a later version.

5. *One representative per bar.* Functions are prepared for exactly one representative per bar. If multiple representatives are needed, for example if we wanted to use all minimal generators, consider adding all of those simplex ids within the one representative list in the `rep` column.


## Filtered simplicial complex viz

Before running analyses, it can be helpful to gain a better understanding of the (filtered) simplicial complex itself.




## Future goals
The goal of this project is to reach beyond basic persistent homology charts into other areas of TDA, as well as creating novel methods for visualizing topological objects and TDA outputs. If you have ideas for the package, please reach out!

## References

[1] Giusti, Chad, et al. ["Clique topology reveals intrinsic geometric structure in neural correlations."](https://www.pnas.org/content/112/44/13455) Proceedings of the National Academy of Sciences 112.44 (2015): 13455-13460.

[2] Petri, Giovanni, et al. ["Topological strata of weighted complex networks."](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0066506) PloS one 8.6 (2013): e66506.

