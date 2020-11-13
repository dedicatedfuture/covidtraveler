$(document).ready(function(){
	console.log('javascript working');



	$('#id_stateChoice').change(function(){
		console.log("state choice selected",$('#id_stateChoice option:selected').text());
		$.ajax({
			type:'POST', 
			url: 'get_county',
			data: {
				state: $('#id_stateChoice option:selected').text()
			}, 
			success: function(){

			}
		})
	});
	

});