// Copyright (c) 2024, Abdulmalek and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bot Wallet User", {
	refresh(frm) {
    },
    setup: function(frm){
        frm.trigger("wallet_user_filter")
    },
    wallet_user_filter:function(frm){
        frm.set_query("wallet_user",function(){
            return{
                "filters":{
                    "custom_self_service": 1,
                }
            };
        });
    }

});
