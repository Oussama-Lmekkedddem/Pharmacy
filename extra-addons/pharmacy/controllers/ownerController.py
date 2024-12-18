from odoo import http
from odoo.exceptions import ValidationError
from odoo import http
from odoo.http import request
class OwnerController(http.Controller):
    @http.route('/owner/create_account', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def create_account(self, **kwargs):
        if http.request.httprequest.method == 'POST':
            name = kwargs.get('name')
            email = kwargs.get('email')
            password = kwargs.get('password')

            try:
                # Use the create_owner method from the model
                http.request.env['pharmacy.owner'].sudo().create_owner(name, email, password)
                return http.request.redirect('/owner/login')
            except ValidationError as e:
                # If a ValidationError occurs, pass the error message to the template
                return http.request.render('pharmacy.owner_logup', {
                    'error': str(e)
                })
            except Exception as e:
                # Catch any other exceptions and pass the error to the template
                return http.request.render('pharmacy.owner_logup', {
                    'error': f"An unexpected error occurred: {str(e)}"
                })

        # For GET request, just render the create account page
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

            # Get the database name from the environment
            db_name = http.request.env.cr.dbname

            # Use the authenticate method to check the user's credentials
            user_id = http.request.env['res.users'].sudo().authenticate(db_name, email, password,
                                                                        user_agent_env=http.request.env)

            if not user_id:
                return http.request.render('pharmacy.owner_login', {
                    'error': 'Invalid email or password.'
                })

            # Fetch the res.users object using the user_id
            user = http.request.env['res.users'].sudo().browse(user_id)

            if not user:
                return http.request.render('pharmacy.owner_login', {
                    'error': 'User not found.'
                })

            # Simulate login (this should be replaced with a real login session)
            http.request.session['user_id'] = user.id
            return http.request.redirect('/owner/owner_page')

        return http.request.render('pharmacy.owner_login')

    @http.route('/owner/owner_page', type='http', auth='user', website=True)
    def owner_page(self, **kwargs):
        user_id = http.request.session.get('user_id')
        if not user_id:
            return http.request.redirect('/owner/login')

        owner = http.request.env['pharmacy.owner'].sudo().search([('user_id', '=', user_id)], limit=1)
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