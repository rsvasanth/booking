function reloadCurrentStateOptions() {
console.log('reloading state options');
var booking ='';
var number_of_person =0;
var from_date ='';
frappe.web_form.on('booking_type',(field,value) =>{
 booking = value;

})
frappe.web_form.on('number_of_person',(field,value) =>{
	 number_of_person = value;
	
	})
frappe.web_form.on('from_date',(field,value) =>{
	 from_date = value;
	
	})
frappe.web_form.on('to_date', (field, value) => {
console.log(field, value);
frappe.call({
    method: 'booking.booking.doctype.booking_desk_reservation.booking_desk_reservation.create_record',
    args:{
		'bookingtype':booking,
		'nop':number_of_person,
		'fromdate':from_date,
		'todate':value
	},
     callback: (r) => {
        // on success
	console.log(r);

	$( "#bookingid" ).html( r.message[0]);
	$( "#member" ).html( 'Name:'+'{{member}} ');
	$( "#duration_start" ).html( 'Starting  Date_:_'+from_date);
	$( "#duration_end" ).html('Ending  Date_:_'+value)
	$( 'h5.total' ).text(+r.message[1])
	frappe.web_form.set_value('amount', r.message[1])
    },
    error: (r) => {
        // on error
		console.log(r);
    }
})
});

}

frappe.ready(function() {
	data = {};
	frappe.web_form.add_button_to_header(" Check Button","",function () {

		frappe.call({
			method: 'booking.booking.doctype.api.api.make_payment',
			args: data,
			callback: function(r) {
				// redirect to razor pay url
				window.location.href = r.message;
			}
		});
	});
	
	// bind events here
	$( "div.demo-container" )
	.html( "<p>All new content. <em>You bet!</em></p>" );
	frappe.web_form.events.on('after_load', reloadCurrentStateOptions);
});