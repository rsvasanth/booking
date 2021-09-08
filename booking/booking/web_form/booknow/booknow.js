function reloadCurrentStateOptions() {
	var booking = '';
	var number_of_person = 0;
	var from_date = '';
	var to_date = '';
	var draft_booking = '';
	var select_person_count=[];
	var guest='';
	var email='';
	var phone='';
	var today= new Date();



	frappe.web_form.on('booking_type', (field, value) => {
		booking = value;

	})

	frappe.web_form.on('from_date', (field, value) => {
		from_date = value;

	})
	frappe.web_form.on('to_date', (field, value) => {

var select_person_count=[];
		to_date = value
		frappe.call({
			method: 'booking.booking.doctype.booking_desk_reservation.booking_desk_reservation.avillable_check',
			args: {
			
				'fromdate':from_date,
				'todate':to_date,
			
			},

			// freeze the screen until the request is completed
			freeze: true,
			callback: (r) => {
				console.log(r)
				const currentStateSelect = $('select[data-fieldname="number_of_person"]');
				currentStateSelect.html('<option></option>');
				if(r.message == 0){
					frappe.msgprint("No Desk Avillable")
				}
				for (let i = 0; i < r.message; i++) {
					console.log(i)
				
					select_person_count.push(i+1)
					currentStateSelect.append($('<option>', {value: select_person_count[i], text: select_person_count[i]}));
				  } 

			},
			error: (r) => {
				// on error
			}
		})
		frappe.web_form.set_value('number_of_person','options', select_person_count)
	})
	frappe.web_form.on('number_of_person', (field, value) => {
		number_of_person = value;
		console.log(number_of_person)
		if(number_of_person =='options'){
		console.log("do nothing")
		}else{
			if(draft_booking > 0){
				frappe.call({
			
					method: 'booking.booking.doctype.booking_desk_reservation.booking_desk_reservation.update_record',
					args:{'draft_booking':booking_value,'qty':value}
					,
					 callback: (r) => {
						// on success
					console.log(r.message[1].item)
			
					$( "#bookingid" ).html( r.message.name);
					$( "#member" ).html( 'Name:'+'{{member}} ');
					$( "#duration_start" ).html( 'Starting  Date_:_'+from_date);
					$( "#duration_end" ).html('Ending  Date_:_'+value)
					$( '#total_amount' ).text(+r.message.net_total)
					frappe.web_form.set_value('amount', r.message.net_total)
			
					},
					error: (r) => {
						// on error
						console.log(r.length);
					}
				})
			}else{
				
				frappe.call({
					method: 'booking.booking.doctype.booking_desk_reservation.booking_desk_reservation.create_record',
					args:{
						'bookingtype':booking,
						'nop':number_of_person,
						'fromdate':from_date,
						'todate':to_date,
						'bookingid':''
					},
					 callback: (r) => {
						// on success
					console.log(r.message[0]);
					console.log(r.message[0].items[0].rate);
					var draft_booking = r.message[0]
					frappe.web_form.set_value('desk_reservation_link', r.message[0])
				
					$( "#bookingid" ).html( r.message[0].name);
					$( "#created" ).html( r.message[0].creation);
					$( "#st_date" ).html( r.message[0].from_date);
					$( "#end_date" ).html( r.message[0].to_date);
					$( "#package" ).html( r.message[0].items[0].item);
					$( "#person" ).html( r.message[0].items[0].qty);
					$( "#price" ).html(r.message[0].items[0].rate);
					$( "#day" ).html()
					$( '#total_amount' ).text(r.message[0].items[0].amount)
					frappe.web_form.set_value('amount', r.message[0].items[0].amount)
					},
					error: (r) => {
						// on error
						console.log(r);
					}
				})
			}
		}


	})
}//end reload current

frappe.ready(function () {
	frappe.web_form.events.on('after_load', reloadCurrentStateOptions);
});