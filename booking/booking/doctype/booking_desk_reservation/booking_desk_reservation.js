// Copyright (c) 2021, kinisi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Booking Desk Reservation', {

	from_date: function(frm) {
		frm.trigger("recalculate_rates");
	},
	to_date: function(frm) {
		frm.trigger("recalculate_rates");
	},
	recalculate_rates: function(frm) {
		if (!frm.doc.from_date || !frm.doc.to_date
			|| !frm.doc.items.length){
			return;
		}
		frappe.call({
			"method": "booking.booking.doctype.booking_desk_reservation.booking_desk_reservation.get_desk_rate",
			"args": {"booking_desk_reservation": frm.doc}
		}).done((r)=> {
			for (var i = 0; i < r.message.items.length; i++) {
				frm.doc.items[i].rate = r.message.items[i].rate;
				frm.doc.items[i].amount = r.message.items[i].amount;
			}
			frappe.run_serially([
				()=> frm.set_value("net_total", r.message.net_total),
				()=> frm.refresh_field("items")
			]);
		});
	},

});

frappe.ui.form.on('Booking Desk Reservation Item', {
	item: function(frm, doctype, name) {
		frm.trigger("recalculate_rates");
	},
	qty: function(frm) {
		frm.trigger("recalculate_rates");
	}
});
