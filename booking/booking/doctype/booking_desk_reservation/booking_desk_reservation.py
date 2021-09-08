# Copyright (c) 2021, kinisi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe import _
from frappe.utils import date_diff, add_days, flt
from frappe.utils.data import new_line_sep
from six import reraise


class BookingDeskUnavailableError(frappe.ValidationError):
    pass


class BookingDeskPricingNotSetError(frappe.ValidationError):
    pass


class BookingDeskReservation(Document):
    def validate(self):
        self.total_desks = {}
        self.set_rates()
        self.validate_availability()

    def validate_availability(self):
        for i in range(date_diff(self.to_date, self.from_date)):
            day = add_days(self.from_date, i)
            self.desks_booked = {}

            for d in self.items:
                if not d.item in self.desks_booked:
                    self.desks_booked[d.item] = 0
                else:
                    print("test")

                desk_type = frappe.db.get_value(
                    "Booking Desk Package", d.item, 'booking_desk_type')
                desks_booked = get_desks_booked(desk_type, day, exclude_reservation=self.name) \
                    + d.qty + self.desks_booked.get(d.item)
                total_desks = self.get_total_desks(d.item)

                if total_desks < desks_booked:
                    frappe.throw(
                        _("Booking Desk of type {0} are unavailable on {1}"
                          ).format(d.item,
                                   frappe.format(day, dict(fieldtype="Date"))),
                        exc=BookingDeskUnavailableError)

                self.desks_booked[d.item] += desks_booked

    def get_total_desks(self, item):
        if not item in self.total_desks:
            self.total_desks[item] = frappe.db.sql(
                """
				select count(*)
				from
					`tabBooking Desk Package` package
				inner join
					`tabBooking Desk` desk on package.booking_desk_type = desk.booking_desk_type
				where
					package.item = %s""", item)[0][0] or 0

        return self.total_desks[item]

    def set_rates(self):
        self.net_total = 0
        for d in self.items:
            net_rate = 0.0
            for i in range(date_diff(self.to_date, self.from_date)):
                day = add_days(self.from_date, i)
                if not d.item:
                    continue
                day_rate = frappe.db.sql(
                    """
					select
						item.rate
					from
						`tabBooking Desk Pricing Item` item,
						`tabBooking Desk Pricing` pricing
					where
						item.parent = pricing.name
						and item.item = %s
						and %s between pricing.from_date
							and pricing.to_date""", (d.item, day))

                if day_rate:
                    net_rate += day_rate[0][0]
                else:
                    frappe.throw(
                        _("Booking  Rate's are not avillable for this period {}").format(
                            frappe.format(day, dict(fieldtype="Date"))),
                        exc=BookingDeskPricingNotSetError)
            d.rate = net_rate
            d.amount = net_rate * flt(d.qty)
            self.net_total += d.amount


@frappe.whitelist(allow_guest=True)
def get_desk_rate(booking_desk_reservation):
    """Calculate rate for each day as it may belong to different Booking Desk Pricing Item"""
    doc = frappe.get_doc(json.loads(booking_desk_reservation))
    doc.set_rates()
    return doc.as_dict()

@frappe.whitelist(allow_guest=True)
def get_desks_booked(desk_type, day, exclude_reservation=None):

    exclude_condition = ''
    if exclude_reservation:
        exclude_condition = 'and reservation.name != {0}'.format(
            frappe.db.escape(exclude_reservation))

    return frappe.db.sql(
        """
		select sum(item.qty)
		from
			`tabBooking Desk Package` desk_package,
			`tabBooking Desk Reservation Item` item,
			`tabBooking Desk Reservation` reservation
		where
			item.parent = reservation.name
			and desk_package.item = item.item
			and desk_package.booking_desk_type = %s
			and reservation.docstatus = 1
			{exclude_condition}
			and %s between reservation.from_date
				and reservation.to_date""".format(exclude_condition=exclude_condition),
        (desk_type, day))[0][0] or 0



@frappe.whitelist(allow_guest=True)
def create_record(bookingtype, nop, fromdate, todate, bookingid):
    if bookingtype == 'Desk Space':
        newbooking = 'desk space package'
    elif bookingtype == 'Conference Room':
        newbooking ='conference room package'

    doc = frappe.get_doc({
        "doctype": "Booking Desk Reservation",
        "guest_name": 'test',
        "from_date": fromdate,
        "to_date": todate,
        "web_booking_id": bookingid
    })
    row = doc.append("items", {})
    row.item = newbooking
    row.qty = int(nop)
    row.rate = ""
    row.amount = ""
    doc.insert()
    return doc,doc.items


@frappe.whitelist(allow_guest=True)
def update_record(draft_booking, qty):
    doc = frappe.get_doc('Booking Desk Reservation', draft_booking)
    for d in doc.items:
        d.qty = int(qty)
    doc.save()
    return doc


def get_current_doc(data):
    frappe.msgprint("Getting current doc..."+data)
    doc = frappe.get_doc('Booking Desk Reservation', '{}'.format(data))
    return doc.items

def get_total_desks(item):
    avillable_count =frappe.db.sql(
                """
				select count(*)
				from
					`tabBooking Desk Package` package
				inner join
					`tabBooking Desk` desk on package.booking_desk_type = desk.booking_desk_type
				where
					package.item = %s""", item)[0][0] or 0
    return avillable_count   

@frappe.whitelist(allow_guest=True)
def avillable_check(todate,fromdate):
    # if item == 'Desk Space':
    #     new_item='Desk Space Package'
    todesk = get_total_desks('Desk Space Package')
    avillable_count =frappe.db.sql(
                """
				select sum(item.qty)
				from
					`tabBooking Desk Package` desk_package,
			        `tabBooking Desk Reservation Item` item,
			        `tabBooking Desk Reservation` reservation
				where
					item.parent = reservation.name
			        and desk_package.item = item.item
			        and desk_package.booking_desk_type = 'Desk'
			        and reservation.docstatus = 1
                    and reservation.from_date < %s
                    and reservation.to_date > %s""",(todate,fromdate))[0][0] or 0
    return todesk - avillable_count



# def validate_availability(self):
#     for i in range(date_diff(self.to_date, self.from_date)):
#         day = add_days(self.from_date, i)
#         self.desks_booked = {}

#         for d in self.items:
#             if not d.item in self.desks_booked:
#                 self.desks_booked[d.item] = 0

#             desk_type = frappe.db.get_value("Booking Desk Package", d.item,
#                                             'booking_desk_type')
#             desks_booked = get_desks_booked(desk_type, day, exclude_reservation=self.name) \
#                 + d.qty + self.desks_booked.get(d.item)
#             total_desks = self.get_total_desks(d.item)
#             print("********* Total Desk avilable")
#             print(total_desks)
#             print("****Total Desk Booked")
#             print(desks_booked)
#             if total_desks < desks_booked:
#                 frappe.throw(
#                     _("Booking Desk of type {0} are unavailable on {1}"
#                       ).format(d.item,
#                                frappe.format(day, dict(fieldtype="Date"))),
#                     exc=BookingDeskUnavailableError)

#             self.desks_booked[d.item] += desks_booked
