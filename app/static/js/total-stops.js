var dnames = ["Bensonhurt, Gravesend", "Corona, Elmhurst, Lefrak City", "Kingsbridge, Marble Hill, Riverdale", "Claremont", "Crown Heights, Prospect Heights", "Fordham, University Heights, Morris Heights", "Broadway Junction, East New York, New Lots", "Murray Hill, Stuyvesant Town", "Midtown, Times Square, Herald's Square", "Olinville, Baychester, Eastchester, Williamsbridge, Woodlawn", "Staten Island North", "Carroll Gardens, Gowanus, Park Slope, Red Hook", "Carroll Gardens, Gowanus, Park Slope, Red Hook", "East Flatbush, Farragut", "Forest Hills, Rego Park", "Coney Island, Brighton Beach", "Kensington, Ocean Parkway", "Belmont, East Tremont, West Farms", "Howard Beach, Lindenwood", "Bronxdale, Morris Park, Pelham Gardens, Pelham Parkway", "Belmont, East Tremont, West Farms", "Forest Hills, Rego Park", "Sunset Park, Windsor Terrace", "Bay Ridge, Fort Hamilton", "Ditmas Park, Flatbush, Midwood", "Bayside, Little Neck, Oakland Gardens", "Soundview, Castle Hill, Parkchester, Unionport", "Flushing, Whitestone, Queensboro Hill, Bay Terrace", "Upper East Side", "Breezy Point, Far Rockaway, The Rockaways, Somerville", "Breezy Point, Far Rockaway, The Rockaways, Somerville", "Corona, Elmhurst, Lefrak City", "Hunt's Point", "Lefferts Gardens", "Carroll Gardens, Gowanus, Park Slope, Red Hook", "Financial District, Tribeca, Wall Street", "Brookville, Floral Park, Laurelton, Queens Village, Rosedale", "Brookville, Floral Park, Laurelton, Queens Village, Rosedale", "Middle Staten Island", "Staten Island South", "Inwood ", "West Harlem, Washington Heights", "Lower East Side, East Village, Chinatown", "Brooklyn Heights, Clinton Hill, DUMBO, Fort Greene", "Kew Gardens, Ozone Park, Richmond Hill, Woodhaven", "Howard Beach, Lindenwood", "Kings Highway, Manhattan Beach, Sheepshead Bay", "Canarsie, Mill Basin", "East Elmhurt, Jackson Heights", "Norwood, Bedford Park", "Kingsbridge, Marble Hill, Riverdale", "Upper West Side, Lincoln Square", "Upper West Side, Lincoln Square", "Concourse, High Bridge", "West Village, SoHo, Greenwich Village", "Chelsea", "Brownsville", "Jamaica,  Briarwood, Fresh Meadows", "Jamaica Center, Hollis, Rochdale, St. Albans", "Long Island City, Sunnyside, Woodside", "Maspeth, Middle Village, Ridgewood", "Bedford-Stuyvesant", "Williamsburg, Greenpoint", "Buschwick", "Central Harlem", "Astoria", "Astoria", "City Island, Co-op city, Pelham Bay, Throgs Neck", "City Island, Co-op city, Pelham Bay, Throgs Neck", "East Harlem", "Mott Haven"];

$(document).ready(function(){
    
        
    var width = 700, height = 800;

    var ids = [35, 46, 20, 15, 32, 17, 29, 6, 5, 24, 57, 59, 30, 41, 48, 37, 36, 18, 55, 23, 18, 48, 31, 34, 38, 53, 21, 49, 8, 56, 56, 46, 14, 33, 2, 1, 55, 55, 58, 59, 12, 9, 3, 26, 51, 52, 39, 42, 45, 19, 20, 7, 7, 16, 4, 4, 40, 50, 54, 44, 47, 27, 25, 28, 10, 43, 43, 22, 22, 11, 13];

    var legend_labels = ['< 2000 stops', '> 2000 stops', '> 5000 stops', '> 10000 stops', '> 13000 stops', '> 17000 stops', '> 21000 stops', '> 25000 stops', '> 30000 stops']

    var color_domain = [2000, 5000, 10000, 13000, 15000, 17000, 21000, 25000, 30000];

    var i = 0;

    var color = d3.scale.threshold()
        .domain([0, 2000, 5000, 10000, 13000, 17000, 21000, 25000, 30000])
        .range(["#f7fbff","#f7fbff","#deebf7","#c6dbef","#9ecae1","#6baed6","#4292c6","#2171b5","#08519c","#08306b"]);

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
            .scale(75000)
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
                d3.select(this.parentNode.appendChild(this)).transition().duration(300)
                    .style({'stroke-opacity':1,'stroke':"#08306b", 'stroke-width':'2'});
                    
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
        .text("Total Number of Stops")

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

        // setInterval(function() {redraw();}, 2000);

        function redraw(){
            ids.forEach(function(r,i){ 
                data.forEach(function(d){
                    if(parseInt(d.communitydistrict) === r){ 
                        rateById[i] = +d.total_stops;
                        hisp[i] = +d.stops_hispanic;
                        black[i] = +d.stops_black;
                        white[i] = +d.stops_white;
                        arr[i] = +d.total_arrests;
                        other[i] = +d.stops_other;
                    }
                });
            })
            
            // d3.select("p").text(years[i]);

            svg.selectAll("#districts")
                .style("fill", function(d, i){return color(rateById[i])});
        };
    };
});