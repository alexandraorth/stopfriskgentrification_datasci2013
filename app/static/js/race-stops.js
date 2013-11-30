$(document).ready(function(){
    var width = 600,
    height = 450;

    var ids = [1, 1,  1,  1,  77,  1, 1, 1, 1, 1, 1, 1 , 76, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 71, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 84, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 79, 1, 83, 1, 1, 1, 1, 1, 1, 1];

    var races = ["B", "W", "A", "I", "P", "Q"];

    var race_name = ["Black", "White", "Asian/Pacific Islander", "American Indian/Alaskan Native", "Black-Hispanic", "White-Hispanic"];

    var legend_labels = ['< 10 stops', '> 300 stops', '> 1000 stops', '> 2000 stops', '> 4000 stops', '> 10000 stops', '> 20000 stops', '> 50000 stops', '> 90000 stops'];

    var color_domain = [10, 300, 1000, 2000, 4000, 10000, 20000, 50000, 90000];

    var i = 0;

    var color = d3.scale.threshold()
        .domain([10, 300, 1000, 2000, 4000, 10000, 20000, 50000, 90000])
        .range(["#e3e3e3", "#ffffd9", "#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"]);

    queue()
        .defer(d3.json, "/static/data/comm_districts.json")
        .defer(d3.csv, "/static/data/race.csv")
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

        var svg = d3.select("#race-stops-map").append("svg")
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
            data.forEach(function(d){ if(d.race === races[i]){rateById[d.addrpct] = +d.count;}});
            
            d3.select("#race-stops-years").text(race_name[i]);
            console.log(rateById)

            svg.selectAll("#districts")
                .style("fill", function(d, i){return color(rateById[ids[i]])});
            i++;
        };
    };
});