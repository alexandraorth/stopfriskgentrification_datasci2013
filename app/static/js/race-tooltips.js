$(document).ready(function(){

    function tooltip_text(addrpct, data){
        /*TODO: add gentrification scores when given*/
        var district = addrpct;
        var white = data.W;
        var asian = data.A;
        var native_american = data.I;
        var black = data.B;
        var hispanic = data.P;
        return "<div id='tooltip'><p>District:"+district+"</p><p>Black:"+black+"<p>White:"+white+"</p><p>Asian:"+asian+"<p>Native American:"+native_american+"</p><p>White-Hispanic:"+hispanic+"</p></div>";

    }
    var width = 600,
    height = 450;

    var ids = [1, 1,  1,  1,  77,  1, 1, 1, 1, 1, 1, 1 , 76, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 71, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 84, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 79, 1, 83, 1, 1, 1, 1, 1, 1, 1];

    var races = ["B", "W", "A", "I", "P", "Q"];

    var race_name = ["Black", "White", "Asian/Pacific Islander", "American Indian/Alaskan Native", "Black-Hispanic", "White-Hispanic"];

    var legend_labels = ['< 10 stops', '> 300 stops', '> 1000 stops', '> 2000 stops', '> 4000 stops', '> 10000 stops', '> 20000 stops', '> 50000 stops', '> 90000 stops'];

    var color_domain = [10, 300, 1000, 2000, 4000, 10000, 20000, 50000, 90000];

    var i = 0;
    var j = 0;

    stops_per_race = {71: {'A': 150, 'B': 30560, 'I': 19, 'Q': 1231, 'P': 482, 'W': 661}, 76: {'A': 675, 'B': 12888, 'I': 92, 'Q': 8634, 'P': 1995, 'W': 5145}, 77: {'A': 538, 'B': 58093, 'I': 64, 'Q': 3894, 'P': 1215, 'W': 1404}, 79: {'A': 821, 'B': 85996, 'I': 191, 'Q': 11749, 'P': 3008, 'W': 3778}, 83: {'A': 502, 'B': 21212, 'I': 132, 'Q': 28523, 'P': 4994, 'W': 2457}, 84: {'A': 672, 'B': 15754, 'I': 87, 'Q': 3641, 'P': 798, 'W': 2566}}


    var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    .text("a simple tooltip");

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
        rrateByColor = {}

        var districts = topojson.feature(nyb, nyb.objects.places).features;

        var projection = d3.geo.mercator()
            .center([-73.9411, 40.6833])
            .scale(290000)
            .translate([(width) / 1.8, (height)/1.8]);

        var path = d3.geo.path()
            .projection(projection);

        var svg = d3.select("#race-tooltips-map").append("svg")
            .attr("width", width)
            .attr("height", height);

        svg.selectAll(".districts")
            .data(districts)
            .enter().append("path")
            .attr("id", "districts")
            .attr("class", function(d,i){ return ids[i]; })
            .attr("d", path)
            .on("mouseover", function(d,i){
    
                tooltip.html(data[i].tooltip_text);return tooltip.style("visibility", "visible");})
            .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
            .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

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


        data.forEach(function(d){ 
                
        });
            
       // setInterval(function() {redraw();}, 2000);

        function redraw(){
            data.forEach(function(d){ 
                console.log(d.addrpct)
                precint = d.addrpct;
                console.log(stops_per_race[precint])
                d.tooltip_text = tooltip_text(precint,stops_per_race[precint]);
            })
        }
    }
    
});