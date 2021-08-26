// Copyright (c) 2016, kinisi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Booking Desk Occupancy"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.now_date(),
			"reqd":1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.now_date(),
			"reqd":1
		}
	]
};
