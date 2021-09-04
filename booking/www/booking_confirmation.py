import frappe

def get_context(context):
    query_params = frappe.local.request.args.get("data")
    print(query_params)
    context.booking = query_params