/* * * * * * * * * * * * * *
*     class StackedVis        *
* * * * * * * * * * * * * */

class StackedVis {
    constructor(parentElement, _data) {
        this.parentElement = parentElement;
        this.data = _data;
        this.displayData = [];
        this.initVis()
    }

    initVis() {
        let vis = this;

        // set the dimensions and margins of the graph
        vis.margin = {top: 10, right: 30, bottom: 100, left: 60};
        vis.width = 800 - vis.margin.left - vis.margin.right;
        vis.height = 400 - vis.margin.top - vis.margin.bottom;

        // append the svg object to the body of the page
        vis.svg = d3.select("#stackedVis")
            .append("svg")
            .attr("width", vis.width + vis.margin.left + vis.margin.right)
            .attr("height", vis.height + vis.margin.top + vis.margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + vis.margin.left + "," + vis.margin.top + ")"); 
                
        /////////////
        // GENERAL //
        /////////////

        // List of groups = header of the csv files
        var keys = vis.data.columns.slice(1)

        // color palette
        var color = d3.scaleOrdinal()
            .domain(keys)
            .range(d3.schemeCategory20c);

        //stack the data?
        var stackedData = d3.stack()
            .keys(keys)
            (vis.data)

        //////////
        // AXIS //
        //////////

        // Add X axis
        var x = d3.scaleLinear()
            .domain([1,24])
            .range([ 0, vis.width ]);
        var xAxis = vis.svg.append("g")
            .attr("transform", "translate(0," + vis.height + ")")
            .call(d3.axisBottom(x).ticks(24))

        // Add X axis label:
        vis.svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", vis.width/2 +80)
            .attr("y", vis.height+40 )
            .text("Time (hour ending)");

        // Add Y axis label:
        vis.svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", 3)
            .attr("dx", "-15em")
            .attr("y", 6)
            .attr("dy", "-2.5em")
            .text("Energy Consumption (Amps)")
            .attr("transform", "rotate(-90)")
            .attr("text-anchor", "start")

          // Add Y axis
        var y = d3.scaleLinear()
            .domain([0,200])
            .range([ vis.height, 0 ]);
        vis.svg.append("g")
            .call(d3.axisLeft(y).ticks(10))


                //////////
        // BRUSHING AND CHART //
                //////////

        // Add a clipPath: everything out of this area won't be drawn.
        var clip = vis.svg.append("defs").append("svg:clipPath")
            .attr("id", "clip")
            .append("svg:rect")
            .attr("width", vis.width )
            .attr("height", vis.height )
            .attr("x", 0)
            .attr("y", 0);
        
        // Add brushing
        var brush = d3.brushX()                 // Add the brush feature using the d3.brush function
            .extent( [ [0,0], [vis.width,vis.height] ] ) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
            .on("end", updateChart) // Each time the brush selection changes, trigger the 'updateChart' function

        // Create the scatter variable: where both the circles and the brush take place
        var areaChart = vis.svg.append('g')
            .attr("clip-path", "url(#clip)")

        // Area generator
        var area = d3.area()
            .x(function(d) { return x(d.data.hour); })
            .y0(function(d) { return y(d[0]); })
            .y1(function(d) { return y(d[1]); })

        // Show the areas
        areaChart
            .selectAll("mylayers")
            .data(stackedData)
            .enter()
            .append("path")
            .attr("class", function(d) { return "myArea " + d.key })
            .style("fill", function(d) { return color(d.key); })
            .attr("d", area)

        // Add the brushing
        areaChart
            .append("g")
            .attr("class", "brush")
            .call(brush);

        var idleTimeout
        function idled() { idleTimeout = null; }

        // A function that update the chart for given boundaries
        function updateChart() {

            var extent = d3.event.selection

            // If no selection, back to initial coordinate. Otherwise, update X axis domain
            if(!extent){
                if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
                x.domain(d3.extent(data, function(d) { return d.year; }))
            }else{
                x.domain([ x.invert(extent[0]), x.invert(extent[1]) ])
                areaChart.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
            }

            // Update axis and area position
            xAxis.transition().duration(1000).call(d3.axisBottom(x).ticks(5))
            areaChart
                .selectAll("path")
                .transition().duration(1000)
                .attr("d", area)
        }

            //////////
        // HIGHLIGHT GROUP //
            //////////

        // What to do when one group is hovered
        var highlight = function(d){
            console.log(d)
            // reduce opacity of all groups
            d3.selectAll(".myArea").style("opacity", .1)
            // expect the one that is hovered
            d3.select("."+d).style("opacity", 1)
        }
    
        // And when it is not hovered anymore
        var noHighlight = function(d){
            d3.selectAll(".myArea").style("opacity", 1)                
        }
  
         //////////
        // LEGEND //
         //////////

        // Add one dot in the legend for each name.
        var size = 5
        vis.svg.selectAll("myrect")
        .data(keys)
        .enter()
        .append("rect")
            .attr("x", 600)
            .attr("y", function(d,i){ return i*(size+5)}) // 100 is where the first dot appears. 25 is the distance between dots
            .attr("width", size)
            .attr("height", size)
            .style("fill", function(d){ return color(d)})
            .on("mouseover", highlight)
            .on("mouseleave", noHighlight)

        // Add one dot in the legend for each name.
        vis.svg.selectAll("mylabels")
        .data(keys)
        .enter()
        .append("text")
            .style("font-size", "7pt")
            .attr("x", 600 + size*1.2)
            .attr("y", function(d,i){ return i*(size+5) + (size/2)}) // 100 is where the first dot appears. 25 is the distance between dots
            .style("fill", function(d){ return color(d)})
            .text(function(d){ return d})
            .attr("text-anchor", "left")
            .style("alignment-baseline", "middle")
            .on("mouseover", highlight)
            .on("mouseleave", noHighlight)
    }
}