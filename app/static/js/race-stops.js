$('.btn').click(function() {
    $('.gentrification').toggle();
  $('.stopfrisk').toggle();
});

$(document).ready(function(){
    var width = 700, height = 800;

    var ids = [35, 46, 20, 15, 32, 17, 29, 6, 5, 24, 57, 59, 30, 41, 48, 37, 36, 18, 55, 23, 18, 48, 31, 34, 38, 53, 21, 49, 8, 56, 56, 46, 14, 33, 2, 1, 55, 55, 58, 59, 12, 9, 3, 26, 51, 52, 39, 42, 45, 19, 20, 7, 7, 16, 4, 4, 40, 50, 54, 44, 47, 27, 25, 28, 10, 43, 43, 22, 22, 11, 13];

    var legend_labels = ['-6', '-4', '-2', '0', '2', '4', '6'];

    var color_domain = [-6, -4, -2, 0, 2, 4, 6];

    var i = 0;

    var color = d3.scale.threshold()
        .domain([-6, -4, -2, 0, 2, 4, 6])
        .range(["#f7fcf5","#e5f5e0","#c7e9c0","#a1d99b","#74c476","#41ab5d","#238b45","#006d2c","#00441b"]);

    queue()
        .defer(d3.json, "/static/data/comm_districts.json")
        .defer(d3.csv, "/static/data/gentrification.csv")
        .await(ready);

    function ready(error, nyb, data){
        var rateById = {};
        rateById[1] = 0;

        var districts = topojson.feature(nyb, nyb.objects.places).features;

        var projection = d3.geo.mercator()
            .center([-73.9411, 40.6833])
            .scale(75000)
            .translate([(width) / 1.8, (height)/1.8]);

        var path = d3.geo.path()
            .projection(projection);

        var svg = d3.select("#race-stops-map").append("svg")
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
                d3.select(this.parentNode.appendChild(this)).transition().duration(300)
                    .style({'stroke-opacity':1,'stroke':"#00441b", 'stroke-width':'2'});   
                
                div.transition()        
                    .duration(200)      
                    .style("opacity", .9);      
                div .html("<p><strong>"+ dnames[i] +"</strong></p><p>Gentrification Index: <span id='value'>" + rateById[i] + "</span></p>")
                    .style("left", (d3.event.pageX) + "px")     
                    .style("top", (d3.event.pageY - 28) + "px");    
            })
            .on("mouseout", function(d) {
                d3.select(this.parentNode.appendChild(this)).transition().duration(300)
                    .style({'stroke-opacity':0,'stroke':'#fff', 'stroke-width':'2'});

                div.transition()        
                    .duration(500)      
                    .style("opacity", 0);   
            });

        var ls_w = 20, ls_h = 20;

        svg.append("text")
            .attr("x", 20)
            .attr("y", function(d, i){ return (i*ls_h) + 4*ls_h;})
            .style("font-size", 25)
            .text("Gentrification by Index");

        var legend = svg.selectAll("g.legend")
            .data(color_domain)
            .enter().append("g")
            .attr("class", "legend");


        legend.append("rect")
            .attr("x", 20)
            .attr("y", function(d, i){ return (i*ls_h) + 5*ls_h;})
            .attr("width", ls_w)
            .attr("height", ls_h)
            .style("fill", function(d, i) { return color(d); })
            .style("opacity", 0.8);

        legend.append("text")
            .attr("x", 50)
            .attr("y", function(d, i){ return (i*ls_h) + ls_h + 95;})
            .text(function(d, i){ return legend_labels[i]; });

        redraw();        

        function redraw(){
            ids.forEach(function(r,i){ 
                data.forEach(function(d){
                    if(parseInt(d.community_district) === r){ 
                        rateById[i] = +d.g_index;
                    }
                });
            })
            
            // d3.select("p").text(years[i]);

            svg.selectAll("#districts")
                .style("fill", function(d, i){return color(rateById[i])});
        };
    };
});