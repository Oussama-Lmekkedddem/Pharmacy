from odoo import http
from odoo.http import request

class OwnerDashboard(http.Controller):

    @http.route('/owner/dashboard', auth='user', website=True)
    def owner_dashboard(self):
        return request.render('pharmacy.owner_dashboard')
