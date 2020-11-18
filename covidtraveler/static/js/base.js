$(document).ready(function(){
	console.log('javascript working');
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

	$('#id_stateChoice').change(function(){
		console.log("state choice selected",$('#id_stateChoice option:selected').text());
		$.ajax({
			headers: { "X-CSRFToken": token },
			type:'POST', 
			url: '/get_county/',
			dataType: "json",
			data: {
				state: $('#id_stateChoice option:selected').text()
			}, 
			csrfmiddlewaretoken: '{{ csrf_token }}', 
			success: function(result){
				console.log('results: ', result);
				var $countyDropDown = $('#id_countyChoice')
				$.each(result, function() {
				    $countyDropDown.update(result.get_county);
				});
			}
		})
	});

});