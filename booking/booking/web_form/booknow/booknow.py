from __future__ import unicode_literals

import frappe


def get_context(context):
    print("*********Hello***********")

    def on_payment_authorized(self, status_changed_to=None):
        self.paid = 1
        self.save(ignore_permissions=True)
    context.username = frappe.session.user
    context.booking = frappe.get_last_doc("Booking Desk Reservation")
    context.bookingid = context.booking.name
    context.member = frappe.session.user
