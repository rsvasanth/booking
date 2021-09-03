# Copyright (c) 2021, kinisi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookingDeskWeb(Document):

    def validate(self):
        print(self.name)

    def on_payment_authorized(self, status_changed_to, task):
        if status_changed_to:
            doc = frappe.get_doc('Booking Desk Web', task)
            doc.paid = 1
            doc.save()
            print(status_changed_to, task)
            doc_temp = frappe.get_doc(
                'Booking Desk Reservation', doc.desk_reservation_link)
            doc_temp.web_booking_id = doc.name
            doc_temp.save()
            doc_temp.submit()
            doc.submit()


@frappe.whitelist()
def get_current_doc_name(self):
    pass
