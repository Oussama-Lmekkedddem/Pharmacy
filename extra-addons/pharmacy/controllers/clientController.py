from odoo import http
from odoo.http import request

class ClientDashboard(http.Controller):

    @http.route('/client/dashboard', auth='user', website=True)
    def client_dashboard(self):
        return request.render('pharmacy.client_dashboard')
