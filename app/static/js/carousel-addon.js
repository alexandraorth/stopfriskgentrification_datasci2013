$(document).ready(function(){
	$('.carousel-control').click(function(){
		cap_div = $("#caption");
		console.log('carousel click')
		setTimeout(function() {
			var number = $('.item.active').attr('id').split('-')[1];
			caption = $('#caption-'+number).html();
			cap_div.html(caption)
		}, 1000);
		

	})

});