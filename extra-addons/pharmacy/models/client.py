from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Client(models.Model):
    _name = 'pharmacy.client'
    _description = 'Client'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    password = fields.Char(string='Password', required=True)
    longitude = fields.Float(string='Longitude')
    latitude = fields.Float(string='Latitude')

    reservations = fields.One2many('pharmacy.reservation', 'client_id', string='Reservations')

    @api.model
    def create_client(self, name, email, password, longitude=None, latitude=None):
        """Create a client and validate required fields"""
        # Validate required fields
        self.validate_name_fields(name)
        self.validate_email_fields(email)
        self.validate_password_fields(password)

        client = self.create({
            'name': name,
            'email': email,
            'password': password,
            'longitude': longitude,
            'latitude': latitude
        })

        client.message_post(body="Client created successfully.")

        return client

    # Update client
    def update_client(self, client_id, name=None, email=None, password=None, longitude=None, latitude=None):
        """Update a client's details and validate required fields"""
        client = self.browse(client_id)

        if not client:
            raise ValidationError("Client not found.")

        if name:
            self.validate_name_fields(name)
        if email:
            self.validate_email_fields(email)
        if password:
            self.validate_password_fields(password)
        if longitude is not None or latitude is not None:
            self.validate_localization_fields(longitude, latitude)

        updated_values = {}
        if name:
            updated_values['name'] = name
        if email:
            updated_values['email'] = email
        if password:
            updated_values['password'] = password
        if longitude is not None:
            updated_values['longitude'] = longitude
        if latitude is not None:
            updated_values['latitude'] = latitude

        if updated_values:
            client.write(updated_values)

        return client

    # Delete client
    def delete_client(self, client_id):
        """Delete a client"""
        client = self.browse(client_id)
        if client:
            client_name = client.name
            client.unlink()
            client.message_post(body=f"Client {client_name} has been successfully deleted.")
            return True
        else:
            raise ValidationError("Client not found.")

    def validate_name_fields(self, name):
        """Validate that the name is provided"""
        if not name:
            raise ValidationError("Name is required.")

    def validate_email_fields(self, email):
        """Validate that the email is provided and in a valid format"""
        if not email:
            raise ValidationError("Email is required.")

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format.")

    def validate_password_fields(self, password):
        """Validate that the password is provided"""
        if not password:
            raise ValidationError("Password is required.")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    def validate_localization_fields(self, longitude, latitude):
        """Validate that the longitude and latitude are valid"""
        if longitude is None or latitude is None:
            raise ValidationError("Longitude and Latitude must be provided if localization is used.")
        if not (-180 <= longitude <= 180):
            raise ValidationError("Longitude must be between -180 and 180 degrees.")
        if not (-90 <= latitude <= 90):
            raise ValidationError("Latitude must be between -90 and 90 degrees.")

    def access_localization(self):
        """Return the longitude and latitude of the client if available"""
        for client in self:
            if client.longitude and client.latitude:
                return {'longitude': client.longitude, 'latitude': client.latitude}
            else:
                raise ValidationError("Localization not available for this client.")