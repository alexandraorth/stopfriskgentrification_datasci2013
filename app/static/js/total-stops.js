$(document).ready(function(){
    var width = 600,
    height = 450;

    var ids = [1, 1,  1,  1,  77,  1, 1, 1, 1, 1, 1, 1 , 76, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 71, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 84, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 79, 1, 83, 1, 1, 1, 1, 1, 1, 1];

    var years = ["2005", "2006", "2007", "2008", "2009", "2010", "2011"];

    var legend_labels = ['< 100 stops', '>1000 stops', '> 3000 stops', '> 5000 stops', '> 7000 stops', '> 9000 stops', '> 11000 stops', '> 13000 stops', '> 18000 stops']

    var color_domain = [100, 1000, 3000, 5000, 7000, 9000, 11000, 13000, 18000];

    var i = 0;

    var color = d3.scale.threshold()
        .domain([100, 1000, 3000, 5000, 7000, 9000, 11000, 13000, 18000])
        .range(["#e3e3e3", "#ffffd9", "#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"]);

    queue()
        .defer(d3.json, "/static/data/comm_districts.json")
        .defer(d3.csv, "/static/data/total_data.csv")
        .await(ready);

    function ready(error, nyb, data){
        var rateById = {};
        rateById[1] = 0;

        var districts = topojson.feature(nyb, nyb.objects.places).features;

        var projection = d3.geo.mercator()
            .center([-73.9411, 40.6833])
            .scale(290000)
            .translate([(width) / 1.8, (height)/1.8]);

        var path = d3.geo.path()
            .projection(projection);

        var svg = d3.select("#total-stops-map").append("svg")
            .attr("width", width)
            .attr("height", height);

        svg.selectAll(".districts")
            .data(districts)
            .enter().append("path")
            .attr("id", "districts")
            .attr("class", function(d,i){ return ids[i]; })
            .attr("d", path)

        var legend = svg.selectAll("g.legend")
            .data(color_domain)
            .enter().append("g")
            .attr("class", "legend");

        var ls_w = 20, ls_h = 20;

        legend.append("rect")
            .attr("x", 20)
            .attr("y", function(d, i){ return height - (i*ls_h) - 2*ls_h;})
            .attr("width", ls_w)
            .attr("height", ls_h)
            .style("fill", function(d, i) { return color(d); })
            .style("opacity", 0.8);

        legend.append("text")
            .attr("x", 50)
            .attr("y", function(d, i){ return height - (i*ls_h) - ls_h - 4;})
            .text(function(d, i){ return legend_labels[i]; });

        redraw();        

        setInterval(function() {redraw();}, 2000);

        function redraw(){
            data.forEach(function(d){ if(d.year === years[i]) rateById[d.id] = + d.count;});
            
            d3.select("p").text(years[i]);

            svg.selectAll("#districts")
                .style("fill", function(d, i){return color(rateById[ids[i]])});
            i++;
        };
    };
});