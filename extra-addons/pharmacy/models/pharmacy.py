from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64

class Pharmacy(models.Model):
    _name = 'pharmacy.pharmacy'
    _description = 'Pharmacy'

    name = fields.Char(string='Name', required=True)
    country = fields.Char(string='Country')
    city = fields.Char(string='City', required=True)
    longitude = fields.Float(string='Longitude', required=True) #digits=(16, 2)
    latitude = fields.Float(string='Latitude', required=True)   #digits=(16, 2)
    documentations = fields.Many2many('ir.attachment', string='Documentations', required=True)
    phone = fields.Char(string='Phone')
    description = fields.Text(string='Description')
    logo = fields.Binary(string='Logo')
    distance = fields.Float(string='Distance', default=0.0)
    is_Online = fields.Boolean(string="Is Online", default=False)

    owner_id = fields.Many2one(
        'pharmacy.owner',
        string='Owner',
        required=True,
        ondelete='cascade',
        index=True
    )

    _sql_constraints = [
        ('owner_pharmacy_uniq', 'unique(owner_id)', 'Each pharmacy can have only one owner.')
    ]

    stocks = fields.One2many('pharmacy.stock', 'pharmacy_id', string='Stocks')

    @api.model
    def unlink(self):
        """When a pharmacy is deleted, its associated stock should also be deleted"""
        for stock in self.stocks:
            stock.unlink()
        return super(Pharmacy, self).unlink()

    @api.model
    def create_pharmacy(self, name, country, city, longitude, latitude, phone=None, description=None,
                        documentations=None, owner_id=None):
        """Create a pharmacy and validate required fields"""
        # Validate required fields
        self.validate_pharmacy_fields(name, country, city, longitude, latitude, documentations)

        logo = self._get_default_logo()

        pharmacy = self.create({
            'name': name,
            'country': country,
            'city': city,
            'longitude': longitude,
            'latitude': latitude,
            'phone': phone,
            'description': description,
            'documentations': documentations,
            'logo': logo,
            'owner_id': owner_id
        })

        pharmacy.message_post(body="Pharmacy created successfully.")
        return pharmacy

    def update_pharmacy(self, pharmacy_id, name=None, country=None, city=None, longitude=None, latitude=None,
                        phone=None, description=None, logo=None, documentations=None):
        """Update the pharmacy's details and validate fields"""
        pharmacy = self.browse(pharmacy_id)

        if not pharmacy:
            raise ValidationError("Pharmacy not found.")

        if name:
            self.validate_pharmacy_fields(name, country, city, longitude, latitude, documentations)

        if not logo:
            logo = self._get_default_logo()

        updated_values = {}
        if name:
            updated_values['name'] = name
        if country:
            updated_values['country'] = country
        if city:
            updated_values['city'] = city
        if longitude:
            updated_values['longitude'] = longitude
        if latitude:
            updated_values['latitude'] = latitude
        if phone:
            updated_values['phone'] = phone
        if description:
            updated_values['description'] = description
        if documentations:
            updated_values['documentations'] = documentations
        if logo:
            updated_values['logo'] = logo

        if updated_values:
            pharmacy.write(updated_values)

        return pharmacy

    def delete_pharmacy(self, pharmacy_id):
        """Delete the pharmacy from the system"""
        pharmacy = self.browse(pharmacy_id)
        if pharmacy:
            pharmacy_name = pharmacy.name
            pharmacy.unlink()

            # for stock in pharmacy.stocks:
            #     stock.unlink()

            pharmacy.message_post(body=f"Pharmacy {pharmacy_name} has been successfully deleted.")
            return True
        else:
            raise ValidationError("Pharmacy not found.")

    def validate_pharmacy_fields(self, name, country, city, longitude, latitude, documentations):
        """Validate that the required fields are provided"""
        if not name:
            raise ValidationError("Name is required.")
        if not country:
            raise ValidationError("Country is required.")
        if not city:
            raise ValidationError("City is required.")
        if longitude is None or latitude is None:
            raise ValidationError("Longitude and Latitude are required.")
        if not documentations:
            raise ValidationError("Documentations are required.")
        if not (-180 <= longitude <= 180):
            raise ValidationError("Longitude must be between -180 and 180.")
        if not (-90 <= latitude <= 90):
            raise ValidationError("Latitude must be between -90 and 90.")

    @api.model
    def _get_default_logo(self):
        default_logo = self.env['ir.attachment'].search([('name', '=', 'default_pharmacy_logo')], limit=1)
        if not default_logo:
            # If no default logo exists, create it programmatically
            try:
                image_path = "../static/logo/default_pharmacy_logo.png"
                with open(image_path, 'rb') as image_file:
                    default_logo_data = base64.b64encode(image_file.read()).decode('utf-8')
            except FileNotFoundError:
                raise ValidationError("The default logo image file was not found at the specified path.")

            # Create the default logo in ir.attachment
            default_logo = self.env['ir.attachment'].create({
                'name': 'default_pharmacy_logo',
                'type': 'binary',
                'datas': default_logo_data,
                'mimetype': 'image/png',
                'res_model': 'pharmacy.pharmacy',
                'res_id': 1,  # This is just a dummy res_id, as it's a default logo used globally
            })
        return default_logo.id