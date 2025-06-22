import frappe
import requests
from property_management.property_management.doctype.property_management_setting.property_management_setting import PropertyManagementSetting
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_lon_lat(name, address):
    setting = PropertyManagementSetting.get_map_api()

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={setting}"
    
    geocode_response = requests.get(url)
    
    if geocode_response.status_code != 200:
        frappe.throw(_("Failed to fetch location data from Google Maps API"))
    
    geocode_data = geocode_response.json()
    
    if geocode_data.get('results'):
        lat = geocode_data['results'][0]['geometry']['location']['lat']
        lng = geocode_data['results'][0]['geometry']['location']['lng']
    else:
        frappe.throw(_("No results found for the location"))
    
    return lat, lng
