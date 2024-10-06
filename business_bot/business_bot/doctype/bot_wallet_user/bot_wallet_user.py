# Copyright (c) 2024, Abdulmalek and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from business_bot.business_bot.api.config import BusinessBotConfigure


class BotWalletUser(Document):
	bbconfig = BusinessBotConfigure()
	def validate(self):
		self.send_welcome_noti()

	def send_welcome_noti(self):
		if self.send_welcome_message == 1:
			message = _(f"Dear : {self.full_name} \n welcome to jawali company bot , Your sevice bot has been activated")
			self.bbconfig.send_whatsapp_message(self.mobile_no,False,False, message)

