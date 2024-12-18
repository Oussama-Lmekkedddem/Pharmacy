from odoo import http
from odoo.http import request

class AdminController(http.Controller):

    @http.route('/admin/dashboard', auth='user')
    def admin_dashboard(self):
        return request.render('pharmacy.admin')




# 1. Admin (Odoo Backend Interface):
# Interface: Odoo backend (default UI for system administration).
# Authentication: auth='admin' to restrict access to superusers only.
# Routing:
# Use routes without website=True, as they are intended for the backend.
# Optionally, define XML menus to make these routes accessible via the Odoo backend navigation.
# Configuration:
#
# auth='admin'
# No website=True.