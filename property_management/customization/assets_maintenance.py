import frappe
from frappe import _

@frappe.whitelist()
def copy_tasks_to_asset(tasks, asset_name):
    tasks = frappe.parse_json(tasks)

    if not asset_name:
        frappe.throw(_("Please select an Asset."))

    if not tasks:
        frappe.throw(_("No tasks found to copy."))

    try:
        asset = frappe.get_doc("Asset", asset_name)

        asset.set("custom_maintenance_history", [])

        for task in tasks:
            asset.append("custom_maintenance_history", {
                "maintenance_task": task.get("maintenance_task"),
                "periodicity":task.get("periodicity"),
                "start_date": task.get("start_date"),
                "end_date": task.get("end_date"),
                "assign_to": task.get("assign_to"),
                "maintenance_type": task.get("maintenance_type"),
                "maintenance_status": task.get("maintenance_status"),
                "certificate_required": task.get("certificate_required"),
                "assign_to_name": task.get("assign_to_name"),
                "next_due_date": task.get("next_due_date"),
                "description": task.get("description"),
                "last_completion_date": task.get("last_completion_date")      
            })

        asset.save()
        frappe.db.commit()

        return _("Tasks copied successfully!")
    except Exception as e:
        frappe.log_error(_("Error copying tasks: {0}").format(str(e)))
        frappe.throw(_("Failed to copy tasks. Please try again."))