# Copyright (c) 2021, kinisi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class BookingDeskPackage(Document):
    def validate(self):
        if not self.item:
            item = frappe.get_doc(dict(
                doctype='Booking Item',
                item_code=self.name,
            ))
            item.insert()
            self.item = item.name
