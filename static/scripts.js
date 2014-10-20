
$(document).ready(function() {

	$('tr.flights').click(function(){
	    if ($(this).hasClass('selected')) {
	    	$(this).removeClass('selected');
	    } else {
			$(this).addClass('selected').siblings().removeClass('selected');
	    }
	});

    $('#submit_flight').on('click', function(e) {
        e.preventDefault()
        var first_name = $('input[name=first_name]').val();
        var last_name = $('input[name=last_name]').val();
        var bags = $('input[name=bags]').val();
        var flight_number = $('.selected').attr('id')
        if (first_name && last_name && bags && flight_number) {
        	submitFlight(first_name, last_name, bags, flight_number)
        	$('.popup').hide()
        }
    })

    $('#select_flight').on('click', function(e) {
        e.preventDefault()
        $('#passenger_form').show()
        $('.black_overlay').show()
    })

	
	$(document).keyup(function(e){
    if(e.keyCode === 27) {
      $('#fade, .popup:visible').fadeOut('normal', function() { $('#fade, .popup:visible').css('display','none')});
      $('.black_overlay').hide()
    }
  	});

});



function submitFlight(first_name, last_name, bags, flight_number) {
	var addUserRequest = $.ajax({
		type: "POST",
		url: "/flight/book",
		data: {first_name: first_name, last_name: last_name, bags: bags, flight_number: flight_number}
	})
	addUserRequest.success(function(data) {
    	$('.popup').hide();
		$("html").append(data);
		clearFields();
		$('#ok').on('click', function(e) {
    		$(this).parent().remove();
    		$('.black_overlay').hide()
    	})
	})
}

function clearFields() {
	$('input').val('');
	$('selected').removeClass('selected')
}