$(document).ready(function(){

	var xdata = [-6, -4, -2, 0, 2, 4];
	var ydata = [0.00226885533333333, 0.00441588688888889, 0.0049220924, 0.0051748516, 0.00764690355555556, 0.00703680057142857];
	var dataset = [[-6, 0.00226885533333333], [-4, 0.00441588688888889], [-2, 0.0049220924], [0, 0.0051748516], [2, 0.00764690355555556], [4, 0.00703680057142857]];
	var ratio = [0.287474082205147, 0.0523345305284761, 0.118375433382863, 0.930062943350984, 0.630132804152038, 0.555132134868694];
	var pointColour = d3.scale.category20b();

	var width = 900;
	var height = 500;

	var y = d3.scale.linear()
		.domain([d3.min(ydata), d3.max(ydata)])
		.range([ height-40, 100]);

	var x = d3.scale.linear()
		.domain([d3.min(xdata) -1, d3.max(xdata) +1])  // the range of the values to plot
		.range([ 20, width-150 ]);

	var svg = d3.select("body")
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

	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left");

	svg.append('g')
		.attr('transform', 'translate(45, 0)')
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
	   	return Math.sqrt(ratio[i]*600);
	   });

	});
