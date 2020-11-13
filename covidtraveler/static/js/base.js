$(document).ready(function(){
	console.log('javascript working');
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;



	$('#id_stateChoice').change(function(){
		console.log("state choice selected",$('#id_stateChoice option:selected').text());
		$.ajax({
			headers: { "X-CSRFToken": token },
			type:'POST', 
			url: '/get_county/',
			data: {
				state: $('#id_stateChoice option:selected').text()
			}, 
			csrfmiddlewaretoken: '{{ csrf_token }}', 
			success: function(){

			}
		})
	});
	

});