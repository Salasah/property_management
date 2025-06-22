frappe.ui.form.on('Asset Maintenance', {
    refresh: function(frm) {
        frm.add_custom_button(__('Copy Maintenance Task'), function() {
            let tasks = frm.doc.asset_maintenance_tasks || [];

            if (tasks.length === 0) {
                frappe.msgprint(__("No tasks found to copy."));
                return;
            }

            frappe.call({
                method: 'property_management.customization.assets_maintenance.copy_tasks_to_asset',
                args: {
                    tasks: tasks,
                    asset_name: frm.doc.asset_name
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(__("Tasks copied successfully!"));
                    }
                }
            });
        });
    }
});