from odoo.exceptions import ValidationError
from odoo import http
from odoo.http import request
import base64
from datetime import datetime, timedelta

class OwnerController(http.Controller):

    @http.route('/owner/create_account', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def create_owner_account(self, **kwargs):
        csrf_token = request.csrf_token()
        if http.request.httprequest.method == 'POST':
            # Extract Owner Data
            owner_data = {
                'name': kwargs.get('owner_name'),
                'email': kwargs.get('owner_email'),
                'password': kwargs.get('owner_password'),
                'carte_id': kwargs.get('carte_id'),
                'address': kwargs.get('owner_address'),
                'phone': kwargs.get('owner_phone'),
            }
            # Extract Pharmacy Data
            pharmacy_data = {
                'name': kwargs.get('pharmacy_name'),
                'country': kwargs.get('pharmacy_country'),
                'city': kwargs.get('pharmacy_city'),
                'longitude': kwargs.get('pharmacy_longitude'),
                'latitude': kwargs.get('pharmacy_latitude'),
                'phone': kwargs.get('pharmacy_phone'),
                'description': kwargs.get('pharmacy_description'),
                'documentations': [],
                'logo': None,
            }

            # Handle documentations
            uploaded_files = http.request.httprequest.files.getlist('pharmacy_documentations')
            for uploaded_file in uploaded_files:
                attachment = http.request.env['ir.attachment'].sudo().create({
                    'name': uploaded_file.filename,
                    'datas': base64.b64encode(uploaded_file.read()),
                    'res_model': 'pharmacy.pharmacy',
                    'type': 'binary',
                })
                pharmacy_data['documentations'].append(attachment.id)

            uploaded_logo = http.request.httprequest.files.get('pharmacy_logo')
            if uploaded_logo:
                pharmacy_data['logo'] = base64.b64encode(uploaded_logo.read())

            try:
                http.request.env['pharmacy.owner'].sudo().create_owner_with_pharmacy(owner_data, pharmacy_data)
                return http.request.redirect('/owner/login')
            except ValidationError as e:
                return http.request.render('pharmacy.owner_logup', {
                    'error': str(e),
                    "csrf_token": csrf_token,
                })
            except Exception as e:
                return http.request.render('pharmacy.owner_logup', {
                    'error': f"An unexpected error occurred: {str(e)}",
                    "csrf_token": csrf_token,
                })

        return http.request.render('pharmacy.owner_logup', {"csrf_token": csrf_token})

    @http.route('/owner/login', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def login(self, **kwargs):
        csrf_token = request.csrf_token()
        if http.request.httprequest.method == 'POST':
            email = kwargs.get('email')
            password = kwargs.get('password')

            if not email or not password:
                return http.request.render('pharmacy.owner_login', {
                    'error': 'Email and password are required!',
                    "csrf_token": csrf_token,
                })

            owner = http.request.env['pharmacy.owner'].sudo().search(
                [('email', '=', email), ('password', '=', password)], limit=1)

            if not owner:
                return http.request.render('pharmacy.owner_login', {
                    'error': 'Invalid email or password.',
                    "csrf_token": csrf_token,
                })

            pharmacy = http.request.env['pharmacy.pharmacy'].sudo().search(
                [('owner_id', '=', owner.id)], limit=1)
            if pharmacy:
                pharmacy.sudo().write({'is_Online': True})


            http.request.session['owner_id'] = owner.id

            return http.request.redirect('/owner/reservation_management')

        return http.request.render('pharmacy.owner_login', {"csrf_token": csrf_token})

    @http.route('/owner/logout', type='http', auth='public', website=True, methods=['POST'])
    def logout(self):
        # Get the logged-in owner ID from the session
        owner_id = http.request.session.get('owner_id')
        if owner_id:
            # Clear the session
            # http.request.session.logout()
            pharmacy = http.request.env['pharmacy.pharmacy'].sudo().search(
                [('owner_id', '=', owner_id)], limit=1)
            if pharmacy:
                pharmacy.sudo().write({'is_Online': False})

        # Redirect to login page
        return http.request.redirect('/owner/login')

    @http.route('/owner/owner_delete', type='http', auth='user', website=True, methods=['POST'])
    def owner_delete(self, **kwargs):
        owner_id = http.request.session.get('owner_id')
        if not owner_id:
            return http.request.redirect('/owner/login')

        # Fetch the owner
        owner = http.request.env['pharmacy.owner'].sudo().browse(owner_id)
        if owner.exists():
            # Use the updated delete_owner method
            owner.sudo().delete_owner(owner_id)

        # Log out the session
        # http.request.session.logout()
        return http.request.redirect('/owner/login')

    @http.route('/owner/reservation_management', type='http', auth='user', website=True)
    def reservation_management(self):
        owner_id = http.request.session.get('owner_id')
        if not owner_id:
            return http.request.redirect('/owner/login')

        # Fetch the pharmacy associated with the owner
        pharmacy = http.request.env['pharmacy.pharmacy'].sudo().search([('owner_id', '=', owner_id)], limit=1)
        if not pharmacy:
            return http.request.redirect('/owner/owner_page')


        if pharmacy.status == 'pending':
            return http.request.render('pharmacy.status_pending')
        elif pharmacy.status == 'declined':
            return http.request.render('pharmacy.status_declined')

        reservations = http.request.env['pharmacy.reservation'].sudo().search(
            [('stock_id.pharmacy_id', '=', pharmacy.id)]
        )

        return http.request.render('pharmacy.owner_reservation', {
            'reservations': reservations
        })

    @http.route('/owner/cancel_reservation', type='http', auth='user', website=True, methods=['POST'])
    def cancel_reservation(self, **kwargs):
        reservation_id = int(kwargs.get('reservation_id', 0))
        reservation = http.request.env['pharmacy.reservation'].sudo().browse(reservation_id)
        if reservation.exists():
            reservation.write({
                'state': 'canceled',
                'cancel_date': datetime.now(),
            })
            reservation.delete_old_reservations()
            return http.request.redirect('/owner/reservation_management')
        else:
            return http.request.redirect('/owner/reservation_management')

    @http.route('/owner/finalize_reservation', type='http', auth='user', website=True, methods=['POST'])
    def finalize_reservation(self, **kwargs):
        reservation_id = int(kwargs.get('reservation_id', 0))
        reservation = http.request.env['pharmacy.reservation'].sudo().browse(reservation_id)
        if reservation.exists():
            stock = reservation.stock_id
            if stock.quantity < reservation.quantity:
                raise ValidationError("Not enough stock to finalize the reservation.")
            stock.quantity -= reservation.quantity

            reservation.write({
                'state': 'finalized',
                'finalized_date': datetime.now(),
            })
            reservation.delete_old_reservations()

        return http.request.redirect('/owner/reservation_management')

    @http.route('/owner/owner_stock', type='http', auth='user', website=True)
    def owner_stock(self):
        owner_id = http.request.session.get('owner_id')
        if not owner_id:
            return http.request.redirect('/owner/login')

        # Fetch owner's pharmacy
        pharmacy = http.request.env['pharmacy.pharmacy'].sudo().search([('owner_id', '=', owner_id)], limit=1)
        if not pharmacy:
            return http.request.render('pharmacy.owner_stock', {
                'error': 'No pharmacy found for the logged-in owner.',
                'stocks': [],
                'medicines': []
            })
        stocks = http.request.env['pharmacy.stock'].sudo().search([('pharmacy_id', '=', pharmacy.id)])
        medicines = http.request.env['pharmacy.medicine'].sudo().search([])

        return http.request.render('pharmacy.owner_stock', {
            'stocks': stocks,
            'medicines': medicines
        })


    @http.route('/owner/manage_stock', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def manage_stock(self, **kwargs):
        owner_id = http.request.session.get('owner_id')
        if not owner_id:
            return http.request.redirect('/owner/login')

        # Fetch owner's pharmacy
        pharmacy = http.request.env['pharmacy.pharmacy'].sudo().search([('owner_id', '=', owner_id)], limit=1)
        if not pharmacy:
            return http.request.redirect('/owner/owner_stock')

        if http.request.httprequest.method == 'POST':
            stock_id = int(kwargs.get('stock_id', 0)) if kwargs.get('stock_id') else None
            medicine_id = int(kwargs.get('medicine_id', 0))
            price = float(kwargs.get('price', 0))
            quantity = int(kwargs.get('quantity', 0))


            medicine = http.request.env['pharmacy.medicine'].sudo().browse(medicine_id)
            if not medicine.exists():
                return http.request.render('pharmacy.owner_stock', {
                    'error': 'Invalid medicine selected.',
                    'stocks': http.request.env['pharmacy.stock'].sudo().search([('pharmacy_id', '=', pharmacy.id)]),
                    'medicines': http.request.env['pharmacy.medicine'].sudo().search([]),
                    'form_data': kwargs
                })


            if stock_id:
                stock = http.request.env['pharmacy.stock'].sudo().browse(stock_id)
                if stock and stock.pharmacy_id.id == pharmacy.id:
                    stock.write({
                        'medicine_id': medicine_id,
                        'price': price,
                        'quantity': quantity
                    })
            else:
                http.request.env['pharmacy.stock'].sudo().create({
                    'pharmacy_id': pharmacy.id,
                    'medicine_id': medicine_id,
                    'price': price,
                    'quantity': quantity
                })

            return http.request.redirect('/owner/owner_stock')


        stock_id = int(kwargs.get('stock_id', 0)) if kwargs.get('stock_id') else None
        stock_data = None
        if stock_id:
            stock = http.request.env['pharmacy.stock'].sudo().browse(stock_id)
            if stock.exists() and stock.pharmacy_id.id == pharmacy.id:
                stock_data = {
                    'stock_id': stock.id,
                    'medicine_id': stock.medicine_id.id,
                    'price': stock.price,
                    'quantity': stock.quantity
                }

        # Render the stock management page
        return http.request.render('pharmacy.owner_stock', {
            'stocks': http.request.env['pharmacy.stock'].sudo().search([('pharmacy_id', '=', pharmacy.id)]),
            'medicines': http.request.env['pharmacy.medicine'].sudo().search([]),
            'form_data': stock_data
        })

    # Delete Stock
    @http.route('/owner/delete_stock', type='http', auth='user', website=True, methods=['POST'])
    def delete_stock(self, **kwargs):
        owner_id = http.request.session.get('owner_id')
        if not owner_id:
            return http.request.redirect('/owner/login')

        # Fetch owner's pharmacy
        pharmacy = http.request.env['pharmacy.pharmacy'].sudo().search([('owner_id', '=', owner_id)], limit=1)
        if not pharmacy:
            return http.request.redirect('/owner/owner_stock')

        # Delete stock
        stock_id = int(kwargs.get('stock_id', 0))
        stock = http.request.env['pharmacy.stock'].sudo().browse(stock_id)
        if stock and stock.pharmacy_id.id == pharmacy.id:
            stock.unlink()

        return http.request.redirect('/owner/owner_stock')

