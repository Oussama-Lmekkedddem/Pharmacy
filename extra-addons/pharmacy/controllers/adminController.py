from odoo import http
from odoo.http import request

class AdminController(http.Controller):

    @http.route('/admin/dashboard', auth='user')
    def admin_dashboard(self):
        return request.render('pharmacy.admin')

