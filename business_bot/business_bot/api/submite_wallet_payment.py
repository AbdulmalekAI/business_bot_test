import frappe 
from frappe import _
from business_bot.business_bot.api.business_bot import BotManager

@frappe.whitelist()
def submit_single_wallet_payment( phone_number,doc_name,pwd):
    bot_class=BotManager(phone_number)
    doctype= "Bot Wallet User"
    doctype="Wallet Payment"
    result= bot_class.submite_doc(doctype,doc_name,pwd)
    return result

    


