# Applied Topology Visualizations

The applied topology visualiation (ApTViz) package contains functions designed to create data graphics from common TDA analyses and structures. Visualization functions rely on some combination of [Plotly](https://plotly.com/python/), JavaScript, [Flask](https://flask.palletsprojects.com/en/1.1.x/), and [D3](https://observablehq.com/@d3). Many of the colors used in these functions are from [Fabio Crameri's colormaps](http://www.fabiocrameri.ch/visualisation.php) [1].


![Example barcode plot with a selction of bars highlighted](/images/barcode_example.png)

Contact [me](https://www.aesizemore.com/) for questions and comments.

<br>

----

<br>

## Table of Contents

* [Expected data organization](https://github.com/asizemore/aptviz#data-organization)
* [Assumptions](https://github.com/asizemore/aptviz#assumptions)
* [Filtered simplicial complex visualizations](https://github.com/asizemore/aptviz#filtered-simplicial-complex-viz)
* [Subcomplex-focused visualizations](https://github.com/asizemore/aptviz#subcomplex-focused-visualizations)
* [PH output viz](https://github.com/asizemore/aptviz#persistent-homology-outputs)

* [Future goals](https://github.com/asizemore/aptviz#future-goals)
* [References](https://github.com/asizemore/aptviz#references)

<br>

## Data organization

These functions expect filtered simplicial complex or barcode data in a specific organizgion:

<br>

`fsc_df` is a [pandas data frame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with one row per simplex and the following columns:

**Required**
* `cell_id`: An integer used to reference the simplex. This number should be unique to the simplex.
* `dim`: An integer *k* denoting the dimension of the $k$-simplex.
* `nodes`: A list of integers denoting the nodes involved in the simplex.
* `faces`: A list of cell ids indicating the faces of the simplex.

**Semi-required**
* `weight`: Float designating simplex weight. See Assumptions section for more information. This column can be ignored if only using the rank of simplices. See function flags for rank vs. weight.
* `rank`: An integer indicating the simplex rank. See [2, 3] for more details. This column can be ignored if only using the weight of simplices. See function flags for rank vs. weight.

**Optional**
* <indicator_col>: Indicator column with entries = 0, 1. Examples include `is_maximal`, in which maximal simplices are marked with 1, and `in_subcomplex`, in which simplices involved in a particular subcomplex are marked with 1.

<br>

`bar_df` is a [pandas data frame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with one row per bar and the following columns:

**Required**
* `bar_id`: An integer used to reference the bar (persistent cycle). This number should be unique to the bar.
* `bar_dim`: An integer *k* denoting the dimension of the persistent $k$-cycle.
* `bar_birth`: Filtration value at which bar is born.
* `bar_death`: Filtration value at which bar dies.

**Optional**
* `rep`: A list of `cell_id`s corresponding to simplices in the associated representative. This column is only used in a subset of plotting functions.
* <indicator_col>: Indicator column with entries = 0,1. Used to highlight bars with a certain property. Examples include `contains_node_of_interest`.
* <continuous_prop>: Column containing a numeric property of each bar. Can be used to provide a color for bars instead `bar_dim`.

<br>

## Assumptions

These functions are particular about data organization (see previous section), but they also make a few assumptions about the data.

1. *Simplex weights are positive.* Most of the code should work regardless, but at this time the functions have not been designed to handle negative weights, specifically.

2. *Simplex weights are ranked highest to lowest.* Following common edge-weighting schemes in the neuroscience and biology, we assume that the highest-weighted simplices are the strongest in the complex.

3. *Simplex weights are unique.* Most functions should work regardless, but currently the code is not designed to handle non-unique weights. This will be removed in a later version.

4. *Simplex ranks are unique.* Most functions should work regardless, but currently the code is not designed to handle non-unique ranks. This will be removed in a later version.

5. *One representative per bar.* Functions are prepared for exactly one representative per bar. If multiple representatives are needed, for example if we wanted to use all minimal generators, consider adding all of those simplex ids within the one representative list in the `rep` column.

<br>

## Filtered simplicial complex viz

Before running analyses, it can be helpful to gain a better understanding of the (filtered) simplicial complex itself. The `exampples_filtered_simplicial_complex.ipynb` notebook illustrates the following functions:
* `fsc_histogram_by_dim(fsc_df, prop = "weight")`
* `fsc_histogram_thresholded(fsc_df, prop = "dim", filter_on = "weight", threshold = 0, keep = "geq")`
* `fsc_attribute_across_filtration(fsc_df, filtration_steps, filtration_col="weight")`

<br>

## Subcomplex-focused visualizations

If there is a particularly interesting set of nodes or simplices (for example, those involving default mode brain regions), see the `examples_subcomplexes.ipynb` notebook for functions that compare properties of a subcomplex to the whole. **Note** requires an indicator column. This notebook demonstrates the following functions:
* `fsc_violin_compare_by_dim(fsc_df, indicator_col, prop = "weight")`
* Faceted histogram using [px.histogram](https://plotly.com/python/histograms/).

<br>

## Persistent homology outputs

The `examples_ph_output.ipynb` notebook contains the following functions used to create persistence diagrams or barcode plots:

* `plot_pd(bar_df, axis_range)`
* `plot_pd_faceted(bar_df, axis_range, col_wrap = 3)`
* `plot_barcode(bar_df, axis_range)`
* `plot_barcode_highlighted(bar_df, axis_range, indicator_col, shaded=False)`
* `plot_barcode_continuous_highlight(bar_df, axis_range, continuous_prop)`


All of the above functions return a [plotly figure object](https://plotly.com/python/figure-structure/) that can be further modified.

<br>

## Future goals
The goal of this project is to reach beyond basic persistent homology charts into other areas of TDA, as well as creating novel methods for visualizing topological objects and TDA outputs. If you have ideas for the package, please reach out!

<br>

## References

[1] Crameri, Fabio, Grace E. Shephard, and Philip J. Heron. "The misuse of colour in science communication." Nature communications 11.1 (2020): 1-10.

[2] Giusti, Chad, et al. ["Clique topology reveals intrinsic geometric structure in neural correlations."](https://www.pnas.org/content/112/44/13455) Proceedings of the National Academy of Sciences 112.44 (2015): 13455-13460.

[3] Petri, Giovanni, et al. ["Topological strata of weighted complex networks."](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0066506) PloS one 8.6 (2013): e66506.

