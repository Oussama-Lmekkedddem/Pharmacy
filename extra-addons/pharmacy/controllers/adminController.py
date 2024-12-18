from odoo import http
from odoo.http import request

class AdminDashboard(http.Controller):

    @http.route('/admin/dashboard', auth='user', website=True)
    def admin_dashboard(self):
        return request.render('pharmacy.admin_dashboard')
