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

            # Search for the client with the provided email and password
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

        # Récupérer les données des pharmacies
        # pharmacies = request.env['pharmacy.pharmacy'].sudo().search([])
        # pharmacy_data = [{
        #     'id': pharmacy.id,
        #     'name': pharmacy.name,
        #     'image': pharmacy.image_url or "/pharmacy/static/logo/default_pharmacy_logo.png",
        #     'is_online': pharmacy.is_online,
        #     'longitude': pharmacy.longitude,
        #     'latitude': pharmacy.latitude
        # } for pharmacy in pharmacies]

        pharmacies = [
            {
                'id': 1,
                'name': "Pharmacie Al Hoceima",
                'image': "/pharmacy/static/logo/default_pharmacy_logo.png",
                'is_online': True,
                'longitude': -3.9370,
                'latitude': 35.2515,
                'distance': 0,
            },
            {
                'id': 2,
                'name': "Pharmacie Fatima",
                'image': "/pharmacy/static/logo/default_pharmacy_logo.png",
                'is_online': True,
                'longitude': -3.9400,
                'latitude': 35.2600,
                'distance': 0,
            },
            {
                'id': 3,
                'name': "Pharmacie Centrale",
                'image': "/pharmacy/static/logo/default_pharmacy_logo.png",
                'is_online': False,
                'longitude': -3.9350,
                'latitude': 35.2540,
                'distance': 0,
            },
            {
                'id': 4,
                'name': "Pharmacie Amine",
                'image': "/pharmacy/static/logo/default_pharmacy_logo.png",
                'is_online': True,
                'longitude': -3.9325,
                'latitude': 35.2530,
                'distance': 0,
            },
            {
                'id': 5,
                'name': "Pharmacie Atlas",
                'image': "/pharmacy/static/logo/default_pharmacy_logo.png",
                'is_online': False,
                'longitude': -3.9380,
                'latitude': 35.2500,
                'distance': 0,
            },
            {
                'id': 6,
                'name': "Pharmacie Rif",
                'image': "/pharmacy/static/logo/default_pharmacy_logo.png",
                'is_online': True,
                'longitude': -3.9405,
                'latitude': 35.2520,
                'distance': 0,
            },
            {
                'id': 7,
                'name': "Pharmacie Florale",
                'image': "/pharmacy/static/logo/default_pharmacy_logo.png",
                'is_online': True,
                'longitude': -3.9390,
                'latitude': 35.2580,
                'distance': 0,
            }
        ]
        stocks = [
            {"id": 1, "name": "Medicine A", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 10.5,
             "quantity": 50},
            {"id": 2, "name": "Medicine B", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 15.0,
             "quantity": 100},
            {"id": 3, "name": "Medicine C", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 7.2,
             "quantity": 25},
            {"id": 4, "name": "Medicine D", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 20.0,
             "quantity": 40},
            {"id": 5, "name": "Medicine E", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 12.0,
             "quantity": 80},
            {"id": 6, "name": "Medicine F", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 9.5,
             "quantity": 60},
            {"id": 7, "name": "Medicine G", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 14.0,
             "quantity": 120},
            {"id": 8, "name": "Medicine H", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 11.3,
             "quantity": 30},
            {"id": 9, "name": "Medicine I", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 13.7,
             "quantity": 90},
            {"id": 10, "name": "Medicine J", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 8.0,
             "quantity": 70},
            {"id": 11, "name": "Medicine K", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 6.5,
             "quantity": 150},
            {"id": 12, "name": "Medicine L", "image": "/pharmacy/static/image/default_medicine_image.png",
             "price": 18.0, "quantity": 20},
        ]

        return self.render_static_html("client_page.html", {
            'client': client,
            'pharmacies': json.dumps(pharmacies),
            'stocks': json.dumps(stocks),
        })

    @http.route('/client/client_medicine', type='http', auth='user', website=True)
    def client_medicine(self):
        client_id = http.request.session.get('client_id')
        if not client_id:
            return request.redirect('/client/login')

        client = request.env['pharmacy.client'].sudo().browse(client_id)
        if not client.exists():
            return request.redirect('/client/login')

        medicine = [
            {'id': 1,
             'idPharmacy': 10,
             'name': "Paracetamol",
             'forme': "Tablet",
             'presentation': "This medicine is presented in a box containing 10 tablets. Each tablet is individually "
                             "sealed within a blister pack to ensure hygiene and protection against environmental "
                             "factors such as humidity and contamination. The box includes detailed usage instructions,"
                             " dosage recommendations, and information about the active ingredients. Suitable for single"
                             " or multiple-dose regimens, this packaging is designed for easy handling and storage.",
             'composition': "Paracetamol 500mg",
             'dosage': "500",
             'unitDosage': "mg",
             'image': "/pharmacy/static/image/default_medicine_image.png",
             'price': 10,
             'amount': 15}
        ]

        stocks = [
            {"id": 1, "name": "Medicine A", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 10.5,
             "quantity": 50},
            {"id": 2, "name": "Medicine B", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 15.0,
             "quantity": 100},
            {"id": 3, "name": "Medicine C", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 7.2,
             "quantity": 25},
            {"id": 4, "name": "Medicine D", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 20.0,
             "quantity": 40},
            {"id": 5, "name": "Medicine E", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 12.0,
             "quantity": 80},
            {"id": 6, "name": "Medicine F", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 9.5,
             "quantity": 60},
            {"id": 7, "name": "Medicine G", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 14.0,
             "quantity": 120},
            {"id": 8, "name": "Medicine H", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 11.3,
             "quantity": 30},
            {"id": 9, "name": "Medicine I", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 13.7,
             "quantity": 90},
            {"id": 10, "name": "Medicine J", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 8.0,
             "quantity": 70},
            {"id": 11, "name": "Medicine K", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 6.5,
             "quantity": 150},
            {"id": 12, "name": "Medicine L", "image": "/pharmacy/static/image/default_medicine_image.png",
             "price": 18.0, "quantity": 20},
        ]

        return self.render_static_html("client_medicine.html", {
            'client': client,
            'medicine': json.dumps(medicine),
            'stocks': json.dumps(stocks),
        })

    @http.route('/client/client_pharmacy', type='http', auth='user', website=True)
    def client_pharmacy(self):
        client_id = http.request.session.get('client_id')
        if not client_id:
            return request.redirect('/client/login')

        client = request.env['pharmacy.client'].sudo().browse(client_id)
        if not client.exists():
            return request.redirect('/client/login')

        pharmacy = [
            {'id': 1,
             'name': "Pharmacie Al Hoceima",
             'country': "Morocco",
             'city': "Casablanca",
             'phone': "+212612345678",
             'description': "This sunny and spacious room is for those traveling light and looking for a comfy and cosy place to lay their head for a night or two. This beach house sits in a vibrant neighborhood littered with cafes, pubs, restaurants and supermarkets and is close to all the major attractions such as Edinburgh Castle and Arthur's Seat.",
             'logo': "/pharmacy/static/logo/default_pharmacy_logo.png",
             'isOnline': True}
        ]

        stocks = [
            {"id": 1, "name": "Medicine A", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 10.5,
             "quantity": 50},
            {"id": 2, "name": "Medicine B", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 15.0,
             "quantity": 100},
            {"id": 3, "name": "Medicine C", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 7.2,
             "quantity": 25},
            {"id": 4, "name": "Medicine D", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 20.0,
             "quantity": 40},
            {"id": 5, "name": "Medicine E", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 12.0,
             "quantity": 80},
            {"id": 6, "name": "Medicine F", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 9.5,
             "quantity": 60},
            {"id": 7, "name": "Medicine G", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 14.0,
             "quantity": 120},
            {"id": 8, "name": "Medicine H", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 11.3,
             "quantity": 30},
            {"id": 9, "name": "Medicine I", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 13.7,
             "quantity": 90},
            {"id": 10, "name": "Medicine J", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 8.0,
             "quantity": 70},
            {"id": 11, "name": "Medicine K", "image": "/pharmacy/static/image/default_medicine_image.png", "price": 6.5,
             "quantity": 150},
            {"id": 12, "name": "Medicine L", "image": "/pharmacy/static/image/default_medicine_image.png",
             "price": 18.0, "quantity": 20},
        ]


        return self.render_static_html("client_pharmacy.html", {
            'client': client,
            'pharmacy': json.dumps(pharmacy),
            'stocks': json.dumps(stocks),
        })
