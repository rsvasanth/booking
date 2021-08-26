# Copyright (c) 2021, kinisi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookingDeskWeb(Document):
    def on_payment_authorized(self, status_changed_to=None):
        self.paid = 1
        self.save(ignore_permissions=True)
