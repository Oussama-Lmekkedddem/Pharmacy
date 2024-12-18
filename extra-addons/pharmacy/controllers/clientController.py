from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class ClientController(http.Controller):
    @http.route('/api/client/create', type='json', auth='user', methods=['POST'])
    def create_client(self, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        password = kwargs.get('password')
        longitude = kwargs.get('longitude')
        latitude = kwargs.get('latitude')

        client = request.env['pharmacy.client'].create_client(name, email, password, longitude, latitude)
        return {'id': client.id, 'name': client.name}

    @http.route('/api/client/update/<int:client_id>', type='json', auth='public', methods=['PUT'])
    def update_client(self, client_id, **kwargs):
        client = request.env['pharmacy.client'].browse(client_id)
        if not client:
            raise ValidationError("Client not found.")
        updated_client = client.update_client(client_id, **kwargs)
        return {'id': updated_client.id, 'name': updated_client.name}

    @http.route('/api/client/delete/<int:client_id>', type='json', auth='public', methods=['DELETE'])
    def delete_client(self, client_id):
        client = request.env['pharmacy.client'].browse(client_id)
        if client:
            client_name = client.name
            client.unlink()
            return {'message': f"Client {client_name} has been successfully deleted."}
        else:
            return {'error': "Client not found."}

    @http.route('/api/client/get/<int:client_id>', type='json', auth='public', methods=['GET'])
    def get_client_by_id(self, client_id):
        client = request.env['pharmacy.client'].browse(client_id)
        if client:
            return {'id': client.id, 'name': client.name, 'email': client.email}
        else:
            return {'error': "Client not found."}

    @http.route('/api/client/get-all', type='json', auth='public', methods=['GET'])
    def get_all_clients(self):
        clients = request.env['pharmacy.client'].search([])
        return [{'id': client.id, 'name': client.name, 'email': client.email} for client in clients]

    @http.route('/api/client/login', type='json', auth='public', methods=['POST'])
    def login(self, email, password):
        client = request.env['pharmacy.client'].search([('email', '=', email), ('password', '=', password)])
        if client:
            return {'message': 'Login successful', 'client_id': client.id}
        else:
            return {'error': 'Invalid credentials'}

    @http.route('/api/client/logout', type='json', auth='public', methods=['POST'])
    def logout(self):
        return {'message': 'Logout successful'}



'''
    3. Client (Angular Frontend Interface):
    Interface: Angular app, no direct access to Odoo backend.
    Authentication:
        Use an API with auth='public' or auth='none' for lightweight, stateless access.
        Rely on Angular for handling the client-side authentication.
    Routing:
        Use auth='public' or auth='none' for Odoo HTTP APIs that the Angular app will call.
        Define JSON endpoints to serve data to the Angular app.
    Configuration:
        auth='public' (or auth='none' for stateless APIs).
        No website=True.
'''