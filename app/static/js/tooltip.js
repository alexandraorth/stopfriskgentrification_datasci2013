 $(document).ready(function(){

    var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    .style("font-size","5px")
    .text("a simple tooltip");
    
	$('#carousel').carousel({  
	  interval: false // in milliseconds  
	});
});