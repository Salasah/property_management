# Copyright (c) 2025, Savan S. Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PropertyManagementSetting(Document):
	
	def get_map_api():
		api = frappe.db.get_single_value("Property Management Setting", "map_api")
		return api
