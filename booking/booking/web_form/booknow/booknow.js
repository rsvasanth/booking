function reloadCurrentStateOptions() {
	var booking ='';
    var number_of_person =0;
    var from_date ='';
	var draft_booking='';

	function CreateBooking(){

		frappe.call({
			method: 'booking.booking.doctype.booking_desk_reservation.booking_desk_reservation.create_record',
			args:{
				'bookingtype':booking,
				'nop':number_of_person,
				'fromdate':from_date,
				'todate':value,
				'bookingid':''
			},
			 callback: (r) => {
				// on success
			console.log(r);
			var draft_booking = r.message[0]
			frappe.web_form.set_value('desk_reservation_link', r.message[0])
		
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

	} //end creating booking 

	function UppdateBooking(booking_value,value) {

		frappe.call({
			
			method: 'booking.booking.doctype.booking_desk_reservation.booking_desk_reservation.update_record',
			args:{'draft_booking':booking_value,'qty':value}
			,
			 callback: (r) => {
				// on success
			console.log(r.message.net_total,r.message.name)
	
			$( "#bookingid" ).html( r.message.name);
			$( "#member" ).html( 'Name:'+'{{member}} ');
			$( "#duration_start" ).html( 'Starting  Date_:_'+from_date);
			$( "#duration_end" ).html('Ending  Date_:_'+value)
			$( 'h5.total' ).text(+r.message.net_total)
			frappe.web_form.set_value('amount', r.message.net_total)

			},
			error: (r) => {
				// on error
				console.log(r.length);
			}
		})

	}
    frappe.web_form.on('booking_type',(field,value) =>{
     booking = value;
    
    })
    frappe.web_form.on('number_of_person',(field,value) =>{
         number_of_person = value;
		 to_date_value = frappe.web_form.get_value('to_date');
		 if (!to_date_value) {

			
		
		 }else{
		
		
		 var booking_value = frappe.web_form.get_value('desk_reservation_link');
		 UppdateBooking(booking_value,value);
		
		
		}


        
        })
    frappe.web_form.on('from_date',(field,value) =>{
         from_date = value;
        
        })
    frappe.web_form.on('to_date',(field,value) =>{
		
		frappe.call({
			
			method: 'booking.booking.doctype.booking_desk_reservation.booking_desk_reservation.avillable_check',
			args:{'item':booking}
			,
			 callback: (r) => {
				// on success
		
				console.log(r)
	

			},
			error: (r) => {
		
			}
		})



})
}

frappe.ready(function() {
	frappe.web_form.events.on('after_load', reloadCurrentStateOptions);
});