var dnames = ["Brooklyn District 11", "Bronx District 4", "0", "Bronx District 3", "Brooklyn District 8", "Bronx District 5", "Brooklyn District 5", "Manhattan District 6", "Manhattan District 5", "Bronx District 12", "Staten Island District 1", "0", "Brooklyn District 6", "Brooklyn District 17", "Bronx District 6", "Brooklyn District 13", "Brooklyn District 12", "Bronx District 6", "0", "Bronx District 11", "0", "0", "Brooklyn District 7", "Brooklyn District 10", "Brooklyn District 14", "Bronx District 11", "Bronx District 9", "Bronx District 7", "Manhattan District 8", "Bronx District 14", "0", "0", "Bronx District 2", "Brooklyn District 9", "Manhattan District 2", "Manhattan District 1", "Bronx District 13", "0", "Staten Island District 2", "Staten Island District 3", "Manhattan District 12", "Manhattan District 9", "Manhattan District 3", "Brooklyn District 2", "Bronx District 9", "Bronx District 10", "Brooklyn District 15", "Brooklyn District 18", "Bronx District 3", "Bronx District 7", "Bronx District 8", "Manhattan District 7", "0", "Bronx District 4", "0", "Manhattan District 4", "Brooklyn District 16", "Bronx District 8", "Bronx District 12", "Bronx District 2", "Bronx District 5", "Brooklyn District 3", "Brooklyn District 1", "Brooklyn District 4", "Manhattan District 10", "Bronx District 1", "0", "Bronx District 10", "0", "Manhattan District 11", "Bronx District 1"];

$(document).ready(function(){
    
        
    var width = 700, height = 800;

    var ids = [35, 46, 20, 15, 32, 17, 29, 6, 5, 24, 57, 59, 30, 41, 48, 37, 36, 18, 55, 23, 18, 48, 31, 34, 38, 53, 21, 49, 8, 56, 56, 46, 14, 33, 2, 1, 55, 55, 58, 59, 12, 9, 3, 26, 51, 52, 39, 42, 45, 19, 20, 7, 7, 16, 4, 4, 40, 50, 54, 44, 47, 27, 25, 28, 10, 43, 43, 22, 22, 11, 13];

    // var years = ["2005", "2006", "2007", "2008", "2009", "2010", "2011"];

    var legend_labels = ['< 2000 stops', '> 2000 stops', '> 5000 stops', '> 10000 stops', '> 13000 stops', '> 17000 stops', '> 21000 stops', '> 25000 stops', '> 30000 stops']

    var color_domain = [2000, 5000, 10000, 13000, 15000, 17000, 21000, 25000, 30000];

    var i = 0;

    var color = d3.scale.threshold()
        .domain([0, 2000, 5000, 10000, 13000, 17000, 21000, 25000, 30000])
        .range(["#ffffff", "#f7fbff","#deebf7","#c6dbef","#9ecae1","#6baed6","#4292c6","#2171b5","#08519c","#08306b"]);

    queue()
        .defer(d3.json, "/static/data/comm_districts.json")
        .defer(d3.csv, "/static/data/nonnormfinal.csv")
        .await(ready);

    function ready(error, nyb, data){
        console.log(data);
        var rateById = {};
        var hisp = {};
        var black = {};
        var white = {};
        var other = {};
        var arr = {};
        rateById[1] = 0;

        var districts = topojson.feature(nyb, nyb.objects.places).features;

        var projection = d3.geo.mercator()
            .center([-73.9411, 40.6833])
            .scale(70000)
            .translate([(width) / 1.8, (height)/1.8]);

        var path = d3.geo.path()
            .projection(projection);

        var svg = d3.select("#total-stops-map").append("svg")
            .attr("width", width)
            .attr("height", height);

        var div = d3.select("body").append("div")   
            .attr("id", "tooltip")               
            .style("opacity", 0);

        svg.selectAll(".districts")
            .data(districts)
            .enter().append("path")
            .attr("id", "districts")
            .attr("class", function(d,i){ return ids[i]; })
            .attr("d", path)
            .on("mouseover", function(d,i) { 

                div.transition()        
                    .duration(200)      
                    .style("opacity", .9);      
                div .html("<p><strong>"+ dnames[i] +"</strong></p>" +
                    "<p>Total Number of Stops: <span id='value'>" + rateById[i] + "</span></p>" +
                    "<p>Black Stopped <span id='value'>" + ((black[i]/rateById[i])*100).toFixed(2) + "</span>%</p>" +
                    "<p>White Stopped: <span id='value'>" + ((white[i]/rateById[i])*100).toFixed(2) + "</span>%</p>" + 
                    "<p>Hispanic Stopped: <span id='value'>" +(( hisp[i]/rateById[i])*100).toFixed(2) + "</span>%</p>" +
                    "<p>Other Stopped: <span id='value'>" + ((other[i]/rateById[i])*100).toFixed(2) + "</span>%</p>" + 
                    "<p>Arrested: <span id='value'>" + ((arr[i]/rateById[i])*100).toFixed(2) + "</span>%</p>")
                    .style("left", (d3.event.pageX) + "px")    
                    .style("top", (d3.event.pageY - 28) + "px");    
            })
            .on("mouseout", function(d) {       
                div.transition()        
                    .duration(500)      
                    .style("opacity", 0);   
            });


        var legend = svg.selectAll("g.legend")
            .data(color_domain)
            .enter().append("g")
            .attr("class", "legend");

        var ls_w = 20, ls_h = 20;

        legend.append("rect")
            .attr("x", 20)
            .attr("y", function(d, i){ return (i*ls_h) + 2*ls_h;})
            .attr("width", ls_w)
            .attr("height", ls_h)
            .style("fill", function(d, i) { return color(d); })
            .style("opacity", 0.8);

        legend.append("text")
            .attr("x", 50)
            .attr("y", function(d, i){ return (i*ls_h) + ls_h + 34;})
            .text(function(d, i){ return legend_labels[i]; });

        redraw();        

        // setInterval(function() {redraw();}, 2000);

        function redraw(){
            ids.forEach(function(r,i){ 
                data.forEach(function(d){
                    // console.log(i); 
                    // console.log(r);
                    if(parseInt(d.communitydistrict) === r){ 
                        // console.log("whale")
                        // console.log(d.total_stops)
                        rateById[i] = +d.total_stops;
                        hisp[i] = +d.stops_hispanic;
                        black[i] = +d.stops_black;
                        white[i] = +d.stops_white;
                        arr[i] = +d.total_arrests;
                        other[i] = +d.stops_other;
                        console.log(r + " " + d.communitydistrict + " " + rateById[i])
                        console.log(d)
                    }
                });
            })
            
            console.log(rateById)

            // d3.select("p").text(years[i]);

            svg.selectAll("#districts")
                .style("fill", function(d, i){return color(rateById[i])});
        };
    };
});