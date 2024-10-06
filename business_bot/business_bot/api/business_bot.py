import frappe
from frappe import _
from frappe.utils import now_datetime
from business_bot.business_bot.api.config import BusinessBotConfigure
# here i'll save the function that is usually used in the bot processes



class BotManager:
	fields = ["name","wallet_company","payment_channel","remittance_provider","recipient","recipient_phone","amount","fee_amount","currency"]

	def __init__(self,phone_number):
		self.phone_number=phone_number
		self.bot_config=BusinessBotConfigure()
		if self.check_client_exist():
			self.wallet_user_doc=self.check_client_exist()
			self.wallet_user=self.wallet_user_doc.wallet_user
			self.creator = self.wallet_user_doc.full_name
			self.wallet_company= self.wallet_user_doc.wallet_company
			self.role=self.wallet_user_doc.role
			self.wallet_checker_phone=self.get_wallet_checker_phone(self.wallet_company)  
			  
		
	def check_client_exist(self):
		doc_name=frappe.db.get_value("Bot Wallet User",{"mobile_no":self.phone_number})
		if doc_name:
			bot_wallet_user_doc =self.get_document("Bot Wallet User",{"mobile_no":self.phone_number})
			return bot_wallet_user_doc
		else :
			return None
		
	
	def get_document(self,doctype,args):
		doc_name=frappe.db.get_value(doctype,args)
		if doc_name:
			return frappe.get_doc(doctype,doc_name)
		else:
			return None
		
	def create_document(self, doctype, **kwargs):
		doc = frappe.get_doc({**kwargs,"doctype": doctype,})
		doc.insert()
		self.send_approvement_noti(doc,self.role,self.wallet_checker_phone)
		return doc
	  
	def _create_doc(self, doctype, **kwargs):
		doc = frappe.get_doc({'doctype': doctype, **kwargs})
		doc.insert()
		return doc
		
	def get_wallet_checker_phone(self,wallet_company):
		return frappe.db.get_value("Bot Wallet User",{"wallet_company":wallet_company,"role":"Wallet Checker"},"mobile_no")
		
		
		
	

	
	def send_approvement_noti(self,doc,role,wallet_checker_phone):
		if role =="Wallet Maker":
			context = self.setup_operation_context(doc)
			return self.bot_config.send_menu_select(
								wallet_checker_phone, False, 
								context["content"],
								context["sections"], 
								context["button_text"])
		else: 
			return _("the role in not wallet maker")

		
	def get_message_metadata(self,doc=None,title=None,description=None):
		title = _("Operation Approval")
		description = _("Are you sure you want to approve this operation?")
		return title, description
	
	def get_doc_message(self, doc, spilt=": ", line_spilt="\n"):
		if isinstance(self.fields, (list, tuple)):
			fields = self.fields
		else:
			fields = doc.meta.get_fieldnames_with_value()
		message = []
		for i in fields  :
			message.append(f"{(doc.meta.get_label(i))}{spilt}{doc.get(i)}")
		return line_spilt.join(message)
	
	def submite_doc(self,doctype,name,pwd):
		bwu="Bot Wallet User"
		if not self.submit_validate(bwu):
			return {
				"code": 403,
				"process": "failed",
				"message": "Validation failed"
			}
		if not self.confirm_password_transaction(pwd):
				return {
					"code": 401,
					"process": "failed",
					"message": "Password confirmation failed"
				}
		try:
			doc = frappe.get_doc(doctype, {"name": name})
			doc.submit()
			return {
				"code": 200,
				"process": "Success",
				"data": _(f"The remittance status is {doc.status}"),
				"wallet_payment": doc.as_dict()
			}
		except Exception as e:
				return {
					"code": 500,
					"process": "failed",
					"message": str(e)
				}
				

		
		
	def confirm_password_transaction(self,pwd):
		"""
		Confirm a password transaction for the current user.
		Args:
			password (str): The password to be confirmed.
		Returns:
			bool: True if the password is confirmed successfully, False otherwise.
		"""
		
		doc = frappe.db.exists("Bot Wallet User",{"mobile_no":self.phone_number})
		if not doc :
			return False
		doc =frappe.get_doc("Bot Wallet User",doc)
		user = doc.user
		return frappe.local.login_manager.check_password(user, pwd)
	
	

	def setup_operation_context(self, doc):
		"""
		Configure operation-specific titles, descriptions, and content messages.
		"""
		title = _("Click here to approve the remittance or reject","Ar")
		# هنا في الوصف يتم ادراج اسم العملية
		description = doc.name
		# هنا يتم ادراج البيانات التي نريد عرضها على الفاحص الذي يقوم بدورة بتأكيد الحوالة
		wp_detailss= self.get_doc_message(doc)
		# هنا في المحتوى يتم ادراج بيانات الحوالة 
		content = _(f"Voucher details as following  : \n {wp_detailss}","ar")

		return {
			"title": title,
			"content": content,
			"sections": [
				{
					"title": _("Options"),
					"rows": [
						{"rowId": "yes", "title": _("Approve the process"), "description": _(description)},
						{"rowId": "no", "title": _("Reject the process"), "description": _(description)}
					]
				}
			],
			"button_text": title
		}
	
	def submit_validate(self,doctype):
		role =frappe.db.exists(doctype,{"mobile_no":self.phone_number})
		if role : 
			role =frappe.get_doc(doctype,role)
			role_m = role.role  
			if role_m == "Wallet Checker" or role_m == "Wallet Main User" or "Wallet Admin":
				return True
			else :
				return False