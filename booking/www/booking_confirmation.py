import frappe

def get_context(context):
    query_params = frappe.local.request.args.get("data")
    doc=frappe.get_doc('Booking Desk Web',query_params)
    print(query_params)
    context.booking_id = doc.name
    context.booking_amount = doc.amount
    context.booking_type = doc.booking_type
    context.booking_person = doc.number_of_person
    context.booking_start = doc.from_date
    context.booking_end = doc.to_date