import frappe 
from frappe import _
from business_bot.business_bot.api.business_bot import BotManager
@frappe.whitelist()
def get_client_information(phone_number):
    bot_class=BotManager(phone_number)
    try:
        if bot_class.check_client_exist():
            return {"code":200,"process":"succes","role":bot_class.role,"data":bot_class.check_client_exist().as_dict()}
        else:
            return {"code":404,"process":"failed","message":_("No client")}
    except Exception as e :
        return {"code":500,"process":"failed","message":str(e)}
    
    