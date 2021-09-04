# Copyright (c) 2021, kinisi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BookingDesk(Document):
	def validate(self):
		if not self.number_of_persons:
			self.number_of_persons = frappe.db.get_value('Booking Desk Type',
					self.booking_desk_type, ['number_of_persons'])
	
