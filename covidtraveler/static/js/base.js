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
				var $countyDropDown = $('#id_countyChoice');
				$countyDropDown.empty();
				for(var i = 0; i < result.length; i++){
					$countyDropDown.append($('<option></option>').val(result[i].county).text(result[i].county));
				}
			}
		})
	});

});