import frappe
from frappe.utils import today

def cron():
    current_date = today()
    
    asset_schedules = frappe.get_all(
        "Asset Depreciation Schedule",
        fields=["name", "asset", "company"]
    )
    
    for asset_schedule in asset_schedules:
        company_name = asset_schedule["company"]
        
        company = frappe.get_doc("Company", company_name)
        depreciation_acc = company.depreciation_expense_account
        accumulated_depreciation_account = company.accumulated_depreciation_account
        
        schedules = frappe.get_all(
            "Depreciation Schedule",
            filters={
                "parent": asset_schedule["name"],
                "schedule_date": current_date
            },
            fields=["name", "depreciation_amount", "journal_entry"]
        )        
        
        for schedule in schedules:
            if not schedule.get("journal_entry"):
                journal_entry = frappe.get_doc({
                    "doctype": "Journal Entry",
                    "posting_date": current_date,
                    "voucher_type":"Depreciation Entry",
                    "accounts": [
                        {
                            "account": accumulated_depreciation_account,
                            "debit_in_account_currency": schedule["depreciation_amount"],
                            "credit_in_account_currency": 0,
                            "reference_type" : "Property",
                            "reference_name": asset_schedule.get('asset')
                        },
                        {
                            "account": depreciation_acc,
                            "debit_in_account_currency": 0,
                            "credit_in_account_currency": schedule["depreciation_amount"],
                        }
                    ],
                    "user_remark": f"Note: Depreciation Entry {asset_schedule.get('asset')} worth {schedule.depreciation_amount}"
                })
                journal_entry.insert()
                frappe.db.set_value("Depreciation Schedule", schedule["name"], "journal_entry", journal_entry.name)
                frappe.db.commit()
                return journal_entry