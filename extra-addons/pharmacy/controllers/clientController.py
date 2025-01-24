from odoo import http
from odoo.exceptions import ValidationError

from odoo.http import request
from jinja2 import Template
import json
import os

class ClientController(http.Controller):
    def render_static_html(self, file_path, context):
        full_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'html', file_path)
        full_path = os.path.abspath(full_path)
        print(f"Resolved Path: {full_path}")
        with open(full_path, "r") as file:
            template = Template(file.read())
        return template.render(context)

    @http.route('/client/create_account', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def create_client_account(self, **kwargs):
        csrf_token = http.request.csrf_token()
        if request.httprequest.method == 'POST':
            name = kwargs.get('name')
            email = kwargs.get('email')
            password = kwargs.get('password')

            try:
                request.env['pharmacy.client'].sudo().create_client(name, email, password)
                return request.redirect('/client/login')
            except ValidationError as e:
                return self.render_static_html("client_logup.html", {
                    "error": str(e),
                    "csrf_token": csrf_token,
                })
            except Exception as e:
                return self.render_static_html("client_logup.html", {
                    "error": f"An unexpected error occurred: {str(e)}",
                    "csrf_token": csrf_token,
                })

        return self.render_static_html("client_logup.html", {"csrf_token": csrf_token})

    @http.route('/client/login', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def login(self, **kwargs):
        csrf_token = request.csrf_token()
        if request.httprequest.method == 'POST':
            email = kwargs.get('email')
            password = kwargs.get('password')

            if not email or not password:
                return self.render_static_html("client_login.html", {
                    "error": "Email and password are required!",
                    "csrf_token": csrf_token,
                })

            client = request.env['pharmacy.client'].sudo().search(
                [('email', '=', email), ('password', '=', password)], limit=1)

            if not client:
                return self.render_static_html("client_login.html", {
                    "error": "Invalid email or password.",
                    "csrf_token": csrf_token,
                })

            request.session['client_id'] = client.id

            return request.redirect('/client/client_page')

        return self.render_static_html("client_login.html", {"csrf_token": csrf_token})

    @http.route('/client/client_page', type='http', auth='user', website=True)
    def client_page(self):
        client_id = http.request.session.get('client_id')
        if not client_id:
            return request.redirect('/client/login')  # Rediriger vers la connexion si non authentifié

        client = request.env['pharmacy.client'].sudo().browse(client_id)
        if not client.exists():
            return request.redirect('/client/login')

        initPharmacies = request.env['pharmacy.pharmacy'].sudo().search([])
        pharmacies = [{
            'id': pharmacy.id,
            'name': pharmacy.name,
            'image': f"/web/image/pharmacy.pharmacy/{pharmacy.id}/logo" if pharmacy.logo else "/pharmacy/static/logo/default_pharmacy_logo.png",
            'is_online': pharmacy.is_Online,
            'longitude': pharmacy.longitude,
            'latitude': pharmacy.latitude,
            'distance': pharmacy.distance,
        } for pharmacy in initPharmacies]

        initStocks = request.env['pharmacy.stock'].sudo().search([])
        stocks = [{
            'id': stock.id,
            'name': stock.medicine_id.name,
            'image': f"/web/image/{stock.medicine_id.images[0].id}"
             if stock.medicine_id.images else
             "/pharmacy/static/image/default_medicine_image.png",
            'price': stock.price,
            'quantity': stock.quantity,
        } for stock in initStocks]

        initReservations = request.env['pharmacy.reservation'].sudo().search([('client_id', '=', client_id)])
        reservations = [{
            'id': reservation.id,
            'name': reservation.stock_id.medicine_id.name,
            'amount': reservation.quantity,
            'price': reservation.price,
        } for reservation in initReservations if reservation.state == 'wait']


        return self.render_static_html("client_page.html", {
            'client': client,
            'pharmacies': json.dumps(pharmacies),
            'stocks': json.dumps(stocks),
            'reservations': json.dumps(reservations),
        })

    @http.route('/client/client_medicine/<int:medicine_id>', type='http', auth='user', website=True)
    def client_medicine(self, medicine_id):
        client_id = http.request.session.get('client_id')
        if not client_id:
            return request.redirect('/client/login')

        client = request.env['pharmacy.client'].sudo().browse(client_id)
        if not client.exists():
            return request.redirect('/client/login')

        initMedicine = request.env['pharmacy.stock'].sudo().browse(medicine_id)
        if not initMedicine.exists():
            return request.not_found()
        medicine = {
            'id': initMedicine.id,
            'idPharmacy': initMedicine.pharmacy_id.id,
            'name': initMedicine.medicine_id.name,
            'forme': initMedicine.medicine_id.forme,
            'presentation': initMedicine.medicine_id.presentation,
            'composition': initMedicine.medicine_id.composition,
            'dosage': initMedicine.medicine_id.dosage,
            'unitDosage': initMedicine.medicine_id.unit_dosage,
            'image': f"/web/image/{initMedicine.medicine_id.images[0].id}"
             if initMedicine.medicine_id.images else
            "/pharmacy/static/image/default_medicine_image.png",
            'price': initMedicine.price,
            'amount': initMedicine.quantity,
        }

        initStocks = request.env['pharmacy.stock'].sudo().search([])
        stocks = [{
            'id': stock.id,
            'name': stock.medicine_id.name,
            'image': f"/web/image/{stock.medicine_id.images[0].id}"
             if stock.medicine_id.images else
            "/pharmacy/static/image/default_medicine_image.png",
            'price': stock.price,
            'quantity': stock.quantity,
        } for stock in initStocks]

        initReservations = request.env['pharmacy.reservation'].sudo().search([('client_id', '=', client_id)])
        reservations = [{
            'id': reservation.id,
            'name': reservation.stock_id.medicine_id.name,
            'amount': reservation.quantity,
            'price': reservation.price,
        } for reservation in initReservations if reservation.state == 'wait']

        return self.render_static_html("client_medicine.html", {
            'client': client,
            'medicine': json.dumps(medicine),
            'stocks': json.dumps(stocks),
            'reservations': json.dumps(reservations),
        })

    @http.route('/client/client_pharmacy/<int:pharmacy_id>', type='http', auth='user', website=True)
    def client_pharmacy(self, pharmacy_id):
        client_id = http.request.session.get('client_id')
        if not client_id:
            return request.redirect('/client/login')

        client = request.env['pharmacy.client'].sudo().browse(client_id)
        if not client.exists():
            return request.redirect('/client/login')

        initPharmacy = request.env['pharmacy.pharmacy'].sudo().browse(pharmacy_id)
        if not initPharmacy.exists():
            return request.not_found()
        pharmacy = {
            'id': initPharmacy.id,
            'name': initPharmacy.name,
            'country': initPharmacy.country if initPharmacy.country else "N/A",
            'city': initPharmacy.city or "N/A",
            'phone': initPharmacy.phone or "N/A",
            'description': initPharmacy.description or "No description available.",
            'logo': f"/web/image/pharmacy.pharmacy/{initPharmacy.id}/logo" if initPharmacy.logo else "/pharmacy/static/logo/default_pharmacy_logo.png",
            'isOnline': initPharmacy.is_Online,
        }

        initStocks = request.env['pharmacy.stock'].sudo().search([('pharmacy_id', '=', pharmacy_id)])
        stocks = [{
            'id': stock.id,
            'name': stock.medicine_id.name,
            'image': f"/web/image/{stock.medicine_id.images[0].id}"
             if stock.medicine_id.images else
            "/pharmacy/static/image/default_medicine_image.png",
            'price': stock.price,
            'quantity': stock.quantity,
        } for stock in initStocks]

        initReservations = request.env['pharmacy.reservation'].sudo().search([('client_id', '=', client_id)])
        reservations = [{
            'id': reservation.id,
            'name': reservation.stock_id.medicine_id.name,
            'amount': reservation.quantity,
            'price': reservation.price,
        } for reservation in initReservations if reservation.state == 'wait']


        return self.render_static_html("client_pharmacy.html", {
            'client': client,
            'pharmacy': json.dumps(pharmacy),
            'stocks': json.dumps(stocks),
            'reservations': json.dumps(reservations),
        })

    @http.route('/client/add_reservation', type='http', auth='public', csrf=False,  website=True, methods=['GET', 'POST'])
    def client_NewReservation(self, **kwargs):
        client_id = http.request.session.get('client_id')
        if not client_id:
            return request.redirect('/client/login')
        client = request.env['pharmacy.client'].sudo().browse(client_id)
        if not client.exists():
            return request.redirect('/client/login')

        if request.httprequest.method == 'POST':
            medicineId = kwargs.get('medicineId')
            amount = kwargs.get('amount')
            price = kwargs.get('price')
            message = kwargs.get('message')

            if not medicineId or not amount or not price:
                return request.redirect(f'/client/client_medicine/{medicineId}?error=missing_fields')

            try:
                amount = int(amount)
                price = float(price)

                request.env['pharmacy.reservation'].sudo().create_reservation(client_id, medicineId, amount, price,
                                                                              message)
                return request.redirect(f'/client/client_medicine/{medicineId}')
            except Exception as e:
                return request.redirect(f'/client/client_medicine/{medicineId}')

        return request.redirect(request.httprequest.referrer or '/client/client_page')

    @http.route('/client/delete_reservation/<int:reservation_id>', type='http', auth='user', website=True)
    def delete_reservation(self, reservation_id, **kwargs):
        client_id = http.request.session.get('client_id')
        if not client_id:
            return request.redirect('/client/login')
        client = request.env['pharmacy.client'].sudo().browse(client_id)
        if not client.exists():
            return request.redirect('/client/login')

        reservation = request.env['pharmacy.reservation'].sudo().browse(reservation_id)
        if not reservation.exists() or reservation.client_id.id != client_id:
            return request.not_found()

        try:
            request.env['pharmacy.reservation'].sudo().delete_reservation(reservation_id)
        except Exception as e:
            return request.redirect(request.httprequest.referrer or '/client/home')

        return request.redirect(request.httprequest.referrer or '/client/client_page')

