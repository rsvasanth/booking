from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import get_url, flt
from frappe.integrations.utils import get_payment_gateway_controller
import urllib


# controller().validate_transaction_currency(currency)

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


@frappe.whitelist(allow_guest=True)
def make_payment():
    # make order - full_name, email, company, amount, workshop=None, conference=None
    # participant = frappe.get_doc({
    #     'doctype': 'Conference Participant',
    #     'full_name': full_name,
    #     'email_id': email,
    #     'company_name': company,
    #     'workshop': workshop,
    #     'conference': conference,
    #     'amount': amount
    # }).insert()

    # get razorpay url
    controller = get_payment_gateway_controller("Razorpay")
    payment_details = {
        "amount": 600,
        "title": "Payment for bill : 111",
        "description": "payment via cart",
        "reference_doctype": "Payment Request",
        "reference_docname": "PR0001",
        "payer_email": "NuranVerkleij@example.com",
        "payer_name": "Nuran Verkleij",
        "order_id": "111",
        "currency": "INR",
        "payment_gateway": "Razorpay"

    }

    url = controller().get_payment_url(**payment_details)
    return url
