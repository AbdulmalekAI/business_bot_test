import frappe 
from business_bot.business_bot.api.business_bot import BotManager
from frappe import _
from company_wallet.company_wallet.report.wallet_company_balance.wallet_company_balance import get_data
@frappe.whitelist()

def create_single_wallet_payment(phone_number,kwargs):
    bot_class=BotManager(phone_number)
    try:
        if not bot_class.check_client_exist():            
            return {"code":404,"process":"failed","message":"No client"}
        elif (bot_class.role == "Wallet Maker"  or bot_class.role=="Admin" or bot_class.role=="Wallet Main User"):
            # adding variable "owner": wallet_user to kwargs
            kwargs["owner"] = bot_class.creator
            kwargs["wallet_company"]=bot_class.wallet_company
            # creating wallet_payment docment
            wallet_payment_doc = bot_class.create_document(doctype="Wallet Payment", **kwargs)
            return{
                "code": 200,
                "process": "success",
                "data": {
                "role": bot_class.role,
                "errors": [],
                "wallet_payment": wallet_payment_doc.as_dict(),
                }}
        else:
            return{
            "code": 404,
            "process": "failed",
            "message": _("This user not allowed to make wallet payment"),
            "errors": ["permittion error"],
        }
    except Exception as e:
        return{
            
                "code": 500,
                "process": "failed",
                "message": e,
                }
    
@frappe.whitelist()
def balance(filters):
    balance = get_data(filters)
    if balance.status:    
        return balance
    

@frappe.whitelist()
def check_status_doc(doctype,doc_name):
    doc=frappe.get_doc(doctype,doc_name)
    return {
        "docstatus":doc.docstatus,
        "status":doc.status,
        "doc":doc.as_dict()
    }