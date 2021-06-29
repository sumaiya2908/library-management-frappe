# Copyright (c) 2021, su and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMembership(Document):

    def before_submit(self):
    	exists = frappe.db.exists(
        	"Library Membership",
        	{
            	"library_member": self.library_member,
            	# check for submitted documents
            	"docstatus": 1,
            	# check if the membership's end date is later than this membership's start date
            	"to_date": (">", self.from_date),
        	},
    	)
    	if exists:
        	frappe.throw("There is an active membership for this member")

		loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
    	self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)