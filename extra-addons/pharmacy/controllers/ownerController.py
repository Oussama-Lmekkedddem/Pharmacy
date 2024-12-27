from odoo.exceptions import ValidationError
from odoo import http
from odoo.http import request

class OwnerController(http.Controller):
    @http.route('/owner/create_account', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def create_owner_account(self, **kwargs):
        if http.request.httprequest.method == 'POST':
            name = kwargs.get('name')
            email = kwargs.get('email')
            password = kwargs.get('password')

            try:
                http.request.env['pharmacy.owner'].sudo().create_owner(name, email, password)
                return http.request.redirect('/owner/login')
            except ValidationError as e:
                return http.request.render('pharmacy.owner_logup', {
                    'error': str(e)
                })
            except Exception as e:
                return http.request.render('pharmacy.owner_logup', {
                    'error': f"An unexpected error occurred: {str(e)}"
                })

        return http.request.render('pharmacy.owner_logup')

    @http.route('/owner/login', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def login(self, **kwargs):
        if http.request.httprequest.method == 'POST':
            email = kwargs.get('email')
            password = kwargs.get('password')

            if not email or not password:
                return http.request.render('pharmacy.owner_login', {
                    'error': 'Email and password are required!'
                })

            owner = http.request.env['pharmacy.owner'].sudo().search(
                [('email', '=', email), ('password', '=', password)], limit=1)

            if not owner:
                return http.request.render('pharmacy.owner_login', {
                    'error': 'Invalid email or password.'
                })

            http.request.session['owner_id'] = owner.id

            return http.request.redirect('/owner/owner_page')

        return http.request.render('pharmacy.owner_login')

    @http.route('/owner/owner_page', type='http', auth='public', website=True)
    def owner_page(self):
        owner_id = http.request.session.get('owner_id')
        if not owner_id:
            return http.request.redirect('/owner/login')

        owner = http.request.env['pharmacy.owner'].sudo().browse(owner_id)
        if not owner.exists():
            http.request.session.logout()
            return http.request.redirect('/owner/login')

        return http.request.render('pharmacy.owner_page', {
            'owner': owner
        })

# @http.route('/owner/dashboard', auth='user')
# def owner_dashboard(self):
#     return request.render('pharmacy.owner')
#

#
#  Owner (Odoo Backend with Login via Angular):
# Interface: Odoo backend interface for each owner.
# Authentication:
# Use auth='user' because owners are regular Odoo users (not superusers).
# Use external authentication (handled by Angular) to log in with email and password and redirect to the Odoo backend.
# Routing:
# Use routes without website=True for the backend.
# Assign specific access rights (e.g., model-level permissions) to ensure owners can only access their own data.
# Configuration:
#
# auth='user'
# No website=True.