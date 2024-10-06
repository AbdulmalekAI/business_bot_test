import string
from frappe.utils import now_datetime
import frappe
import random
from frappe.model.document import Document
class BotOtpCode(Document):
	
	def after_insert(self):
		rand_otp=random.randint(100000, 999999)
		self.otp=rand_otp
		current_datetime_str = frappe.utils.now_datetime().strftime('%Y-%m-%d %H:%M:%S')
		# Convert the current datetime string to a datetime object
		current_datetime = frappe.utils.datetime.datetime.strptime(current_datetime_str, '%Y-%m-%d %H:%M:%S')
		# Add 30 minutes to the current datetime
		expired_at = current_datetime + frappe.utils.datetime.timedelta(minutes=3)
		self.expired_at=expired_at
		self.save()