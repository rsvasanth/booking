from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import get_url, flt
from frappe.integrations.utils import get_payment_gateway_controller
import urllib


@frappe.whitelist()
def make_payment():
    controller = get_payment_gateway_controller("Razorpay")

    payment_details = {
        "amount": 600,
        "title": "Payment for bill : 111",
        "description": "payment via cart",
        "reference_doctype": "Booking Desk Web",
        "reference_docname": "WEB-BOOKING-30-08-2021-00001",
        "payer_email": "NuranVerkleij@example.com",
        "payer_phone_number": "8940515003",
        "payer_name": "Nuran Verkleij",
        "order_id": "111",
        "currency": "INR",
        "payment_gateway": "Razorpay"

    }

    return controller.get_payment_url(**payment_details)

# payment_details = {
#     "amount": 600,
#     "title": "Payment for bill : 111",
#     "description": "payment via cart",
#     "reference_doctype": "Payment Request",
#     "reference_docname": "PR0001",
#     "payer_email": "NuranVerkleij@example.com",
#     "payer_name": "Nuran Verkleij",
#     "order_id": "111",
#     "currency": "INR",
#     "payment_gateway": "Razorpay",
#     "subscription_details": {
#         "plan_id": "plan_12313",  # if Required
#         "start_date": "2018-08-30",
#         "billing_period": "Month"  # (Day, Week, Month, Year),
#         "billing_frequency": 1,
#         "customer_notify": 1,
#         "upfront_amount": 1000
#     }
# }
