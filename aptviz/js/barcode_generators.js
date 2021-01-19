

// Need two svgs - one for the barcode and one for the fsc.
svg_bar = d3.select("#svg_bar")
svg_fsc = d3.select("#svg_fsc")

const width_bar = +svg_bar.attr("width"),
    height_bar = +svg_bar.attr("height");

const width_fsc = +svg_fsc.attr("width"),
    height_fsc = +svg_fsc.attr("height");

const bar_plot_margin = 20,
    fsc_plot_margin = 20;

const bar_margin = 30,
    fsc_margin = 20;


// Colors
const my_charcoal = "#3f4142",
    my_lightgray = "#ebf0f2",
    davos= ['rgb(44, 26, 76)',
       'rgb(40, 59, 110)',
        'rgb(42, 94, 151)',
        'rgb(68, 117, 193)',
        'rgb(96, 137, 190)',
        'rgb(125, 156, 181)',
        'rgb(155, 175, 172)',
        'rgb(186, 196, 163)',
        'rgb(215, 217, 161)',
        'rgb(237, 236, 206)',
        'rgb(255, 255, 255)'];


// Is-clicked indicator
let is_clicked = 0;




d3.json("../data/bar_df.json", function(error1, bar_df) {

    if (error1) throw error1;

    d3.json("../data/fsc_test.json", function(error2,fsc_df) {

        if (error2) throw error2;

        console.log(bar_df)
        console.log(fsc_df)

        // It will be helpful to have just a node data frame
        const node_df = fsc_df.filter(d => {return +d.dim === 0});


        // Define constants read from data UPDATE extract all from data
        const nNodes = node_df.length,
            n_bars = 100,
            filtration_range = [0,300],
            coordinate_range = [0,1];

        // UPDATE creating random layout for nodes -- later create in python and export
        let node_x_coord = [],
            node_y_coord = [];
        
        for (let index = 0; index < nNodes; index++) {
            node_x_coord[index] = Math.random();
            node_y_coord[index] = Math.random();
            
        }



        // Setting barcode axes
        // Set barcode x, y scales UPDATE read domains from data
        const x_bar_scale = d3.scaleLinear()
            .domain([filtration_range[0], filtration_range[1]])
            .range([bar_plot_margin+bar_margin, width_bar - bar_plot_margin - bar_margin]);

        const y_bar_scale = d3.scaleLinear()
            .domain([0, n_bars])
            .range([height_bar-bar_plot_margin - bar_margin, bar_plot_margin + bar_margin]);

        // Set axes for barcode
        const x_axis_bar = d3.axisBottom().scale(x_bar_scale),
            y_axis_bar = d3.axisLeft().scale(y_bar_scale);

        // Draw axes for barcode
        svg_bar.append("g")
            .attr("class", "xaxis")
            .attr("transform", `translate(0,${height_bar-bar_margin})`)
            .call(x_axis_bar);

        svg_bar.append("g")
            .attr("class", "yaxis")
            .attr("transform", `translate(${bar_margin}, 0)`)
            .call(y_axis_bar);

        
        // Setting fsc axes
        // Set fsc x, y scales UPDATE read from data
        const x_fsc_scale = d3.scaleLinear()
            .domain(coordinate_range)
            .range([fsc_margin+fsc_plot_margin, width_fsc - fsc_plot_margin - fsc_margin])
        const y_fsc_scale = d3.scaleLinear()
            .domain(coordinate_range)
            .range([height_fsc - fsc_margin - fsc_plot_margin, fsc_margin+fsc_plot_margin])



        // Draw barcode
        const bars = svg_bar.append("g")
                        .attr("class","barcode")


        bars.selectAll("path")
            .data(bar_df)
            .enter().append("path")
            .attr("d", function(d,i) {return `M ${x_bar_scale(d.bar_birth)},${y_bar_scale(i)} L ${x_bar_scale(d.bar_death)},${y_bar_scale(i)}`})
            .attr("stroke-width",2)
            .attr("stroke",function(d) {return davos[d.bar_dim]})
            .attr("class","bars")
            .on("mouseover",mouseover_bar)
            .on("mouseout",mouseout_bar)
            .on("click",onclick);


        
        // Draw nodes of fsc
        let nodes = svg_fsc.append("g")
            .attr("class","nodes")

        let r = 3;

        nodes.selectAll("circle")
            .data(node_df)
            .enter().append("circle")
                .attr("cx", function(d,i) {return x_fsc_scale(node_x_coord[i]);})
                .attr("cy", function(d,i) {return y_fsc_scale(node_y_coord[i]);})
                .attr("r", r)
                .attr("r0", r)
                .attr("fill","gray")
                .on("mouseover",mouseover_node)
                .on("mouseout",mouseout_node);

        



        // Hover over bars to highlight nodes in fsc
        function mouseover_bar(d) {

            console.log("hovering")

            // Increase stroke width
            let selected_bar = d3.select(this)
            selected_bar.attr("stroke-width",4)

            let highlighted_nodes = highlight_nodes(d);


        }

        function mouseout_bar(d) {

            // Set stroke width back to normal
            let selected_bar = d3.select(this)

            // Stroke-width will have to be a computed value based on the number of bars.
            selected_bar.attr("stroke-width",2)

            // Remove the highlighted nodes
            d3.selectAll(".highlight_nodes").remove();


        }

        // Need a different mouseover and mouseout function if we have clicked on a bar
        function mouseover_bar_clicked(d) {

            let selected_bar = d3.select(this)
            selected_bar.attr("stroke-width",3)
                .attr("stroke", function(d) {return davos[d.bar_dim]})

        }

        function mouseout_bar_clicked(d) {

            // Set stroke width back to normal
            let selected_bar = d3.select(this)

            // Stroke-width will have to be a computed value based on the number of bars.
            selected_bar.attr("stroke-width",2).attr("stroke","gray")

        }


        function onclick(d) {

            // Set all bar fills to gray and to appropriate stroke width
            d3.selectAll(".bars").attr("stroke","gray");
            d3.selectAll(".bars").attr("stroke-width",2);

            // Set THIS bar to bold color
            d3.select(this)
                .attr("stroke",function(d) {return davos[d.bar_dim]})
                .attr("stroke-width",4);

            // Update mouseover and mouseout functions
            d3.selectAll(".bars").on("mouseout",mouseout_bar_clicked);
            d3.select(this).on("mouseout", null);
            d3.selectAll(".bars").on("mouseover",mouseover_bar_clicked)
            d3.select(this).on("mouseover", null);

            // Ensure proper highlight nodes
            d3.selectAll(".highlight_nodes").remove();


            // Highlight nodes
            let highlighted_nodes = highlight_nodes(d);


        };


        function highlight_nodes(d) {

            // Find nodes associated with bar -- NOTE currently we only have four cell_ids per generator
            let generator_nodes = [];
            // console.log(JSON.parse(map_string_to_array(d.rep)))
            for (let index = 0; index < d.rep.length; index++) {
                
                let cell_id = d.rep[index];

                // Find cell_id in fsc data
                let cell_id_nodes = fsc_df.filter(d => {return +d.cell_id === cell_id})[0].nodes

                // Add to generator node list
                generator_nodes.push(...cell_id_nodes);
                
            }


            // Get distinct nodes
            let distinct_generator_nodes = [...new Set(generator_nodes)];

            // Highlight nodes by drawing extra highlight nodes on top of their current positions (makes styling easier)
            let highlighted_nodes = svg_fsc.append("g")
                .attr("class", "highlight_nodes");

            let r = 5;

            highlighted_nodes.selectAll("circle")
                .data(node_df.filter(d => {return distinct_generator_nodes.includes(d.cell_id)}))
                .enter().append("circle")
                    .attr("cx", function(d) {return x_fsc_scale(node_x_coord[d.cell_id]);})
                    .attr("cy", function(d) {return y_fsc_scale(node_y_coord[d.cell_id]);})
                    .attr("r", r)
                    .attr("r0",r)
                    .attr("fill", "orange")
                    .on("mouseover",mouseover_node)
                    .on("mouseout",mouseout_node);

            return highlighted_nodes;


        }

        function mouseover_node() {
            d3.select(this).transition().duration(50).attr("r",8);
        };

        function mouseout_node() {
            let r0 = d3.select(this).attr("r0")
            d3.select(this).transition().duration(50).attr("r",r0)
        }




    });



})






