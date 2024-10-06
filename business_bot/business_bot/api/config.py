import requests
import frappe
from frappe import _, cstr
import urllib.parse

class BusinessBotConfigure:
    def __init__(self):
        self.service_config = frappe.get_doc("Business Bot Config")
        self.session = self.service_config.session
        self.base_url = urllib.parse.urljoin(self.service_config.url, self.session)
        self.token = self.service_config.token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8",
        }    
    
    def send_whatsapp_message(self, phone, is_group, is_newsletter, message):
        try:
            url = f"{self.base_url}/send-message"
            data = {
                "phone": phone,
                "isGroup": is_group,
                "isNewsletter": is_newsletter,
                "message": message,
            }
            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
        except Exception as e:
            frappe.log_error(f"Exception in send_whatsapp_message: {e}")
            return {"status": "error", "message": str(e)}
        
    def send_file(self, phone, is_group, is_newsletter, filename, caption, base64):
        try:
            url = f"{self.base_url}/send-file"
            data = {
                "phone": phone,
                "isGroup": is_group,
                "isNewsletter": is_newsletter,
                "filename": filename,
                "caption": caption,
                "base64": base64
            }
            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
        except Exception as e:
            frappe.log_error(f"Exception in send_menu_select: {e}")
            return {}

    def send_menu_select(self, phone, is_group, description, sections, button_text):
        try:
            url = f"{self.base_url}/send-list-message"
            data = {
                "phone": phone,
                "isGroup": is_group,
                "description": description,
                "sections": sections,
                "buttonText": button_text
            }
            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
        except Exception as e:
            frappe.log_error(f"Exception in send_menu_select: {e}")
            return {}

