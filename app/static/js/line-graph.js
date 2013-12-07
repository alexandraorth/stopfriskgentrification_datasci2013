$(document).ready(function(){

	var xdata = [-6, -4, -2, 0, 2, 4];
	var ydata = [0.00226885533333333, 0.00441588688888889, 0.0049220924, 0.0051748516, 0.00764690355555556, 0.00703680057142857];
	var dataset = [[-6, 0.00226885533333333], [-4, 0.00441588688888889], [-2, 0.0049220924], [0, 0.0051748516], [2, 0.00764690355555556], [4, 0.00703680057142857]];
	var perc = ["4.8% Arrested", "5.1% Arrested", "6.7% Arrested", "6.1% Arrested", "6.2% Arrested", "5.9% Arrested"]
	var ratio = [0.0482191444528549, 0.0519625260695408, 0.0670562454346238, 0.061802489626556, 0.0620555914673562, 0.0591480422271652];
	var pointColour = d3.scale.category20b();

	var width = 900;
	var height = 500;

	var y = d3.scale.linear()
		.domain([d3.min(ydata), d3.max(ydata)])
		.range([ height-40, 100]);

	var x = d3.scale.linear()
		.domain([d3.min(xdata) -1, d3.max(xdata) +1])  // the range of the values to plot
		.range([ 50, width-150 ]);

	var svg = d3.select("#line-graph")
		.append("svg")
		.attr('width', width + 50)
		.attr('height', height + 50);

	var xAxis = d3.svg.axis()
		.scale(x)
		.orient('bottom');

	svg.append('g')
		.attr('transform', 'translate(25,' + height + ')')
		.attr('id', 'xAxis')
		.call(xAxis);

	svg.append("text")      // text label for the x axis
        .attr("x", width/2)
        .attr("y",  height + 40 )
        .style("text-anchor", "middle")
        .text("Gentrification Index");

    svg.append("text")
        .attr("x", width/2)
        .attr("y", 40)
        .style("font-size", 25)
        .style("text-anchor", "middle")
        .text("Average Number of Stops vs Gentrification")

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - 4)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Mean of Total Number of Stops");

    d3.select('svg')
	    .append('text')
	    .attr({'id': 'countryLabel', 'x': 70, 'y': 170})
	    .style({'font-size': '70px', 'font-weight': 'bold', 'fill': '#ddd'});

	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left");

	svg.append('g')
		.attr('transform', 'translate(60, 0)')
		.attr('id', 'yAxis')
		.call(yAxis);

	svg.append('line')
	    .attr('x1',x(dataset[0][0]))
	    .attr('x2',x(dataset[5][0]))
	    .attr('y1',y(dataset[0][1]))
	    .attr('y2',y(dataset[5][1]))
	    .attr("class", "bestfit")

    svg.selectAll("circle")
	   .data(dataset)
	   .enter()
	   .append("circle")
	   .attr('fill', function(d, i) {return pointColour(i);})
	   .attr("cx", function(d) {
        return x(d[0]) + 25; })
	   .attr("cy", function(d) {
	   	return y(d[1]) ;})
	   .attr("r", function(d, i){
	   	return ratio[i]*300;
	   })
	   .on('mouseover', function(d,i) {
	   	console.log(perc[i])
		   	d3.select('svg #countryLabel')
		   	.text(perc[i])
		   	.transition()
		   	.style('opacity', 1);
		   })
	   .on('mouseout', function(d) {
	   	d3.select('svg #countryLabel')
	        .transition()
	        .duration(500)
	        .style('opacity', 0);
	    });

	});
