from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import pandas as pd

class Medicine(models.Model):
    _name = 'pharmacy.medicine'
    _description = 'Medicine'
    _import = True

    name = fields.Char(string='Name', required=True)
    forme = fields.Char(string='Forme')
    presentation = fields.Char(string='Presentation')
    composition = fields.Char(string='Composition')
    dosage = fields.Char(string='Dosage')
    unit_dosage = fields.Char(string='Unit Dosage')
    images = fields.Many2many('ir.attachment', string='Images', domain=[('mimetype', 'in', ['image/jpeg', 'image/png', 'image/gif'])])

    stocks = fields.One2many('pharmacy.stock', 'medicine_id', string='Stocks')

    @api.model
    def unlink(self):
        return super(Medicine, self).unlink()

    @api.model
    def import_medicines_from_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            required_columns = ['name', 'forme', 'presentation', 'composition', 'dosage', 'unit_dosage']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Excel file must contain columns: {required_columns}")
            for _, row in df.iterrows():
                self.create({
                    'name': row['name'],
                    'forme': row['forme'],
                    'presentation': row['presentation'],
                    'composition': row['composition'],
                    'dosage': row['dosage'],
                    'unit_dosage': row['unit_dosage'],
                })
        except Exception as e:
            raise ValueError(f"Error importing Excel file: {e}")


    @api.model
    def create_medicine(self, name, forme=None, presentation=None, composition=None, dosage=None, unit_dosage=None,
                        images=None):
        """Create a medicine and validate fields"""
        # Validate required fields
        self.validate_name_fields(name)

        # Validate optional fields
        self.validate_forme_fields(forme)
        self.validate_presentation_fields(presentation)
        self.validate_composition_fields(composition)
        self.validate_dosage_fields(dosage)
        self.validate_unit_dosage_fields(unit_dosage)

        # Create the medicine record
        medicine = self.create({
            'name': name,
            'forme': forme,
            'presentation': presentation,
            'composition': composition,
            'dosage': dosage,
            'unit_dosage': unit_dosage,
            'images': images
        })

        medicine.message_post(body="Medicine created successfully.")

        return medicine

    # Update Medicine
    def update_medicine(self, medicine_id, name=None, forme=None, presentation=None, composition=None, dosage=None,
                        unit_dosage=None, images=None):
        """Update the medicine's details and validate fields"""
        medicine = self.browse(medicine_id)

        if not medicine:
            raise ValidationError("Medicine not found.")

        # Validate fields based on parameters provided
        if name:
            self.validate_name_fields(name)
        if forme:
            self.validate_forme_fields(forme)
        if presentation:
            self.validate_presentation_fields(presentation)
        if composition:
            self.validate_composition_fields(composition)
        if dosage:
            self.validate_dosage_fields(dosage)
        if unit_dosage:
            self.validate_unit_dosage_fields(unit_dosage)

        # Proceed with updating the fields
        updated_values = {}
        if name:
            updated_values['name'] = name
        if forme:
            updated_values['forme'] = forme
        if presentation:
            updated_values['presentation'] = presentation
        if composition:
            updated_values['composition'] = composition
        if dosage:
            updated_values['dosage'] = dosage
        if unit_dosage:
            updated_values['unit_dosage'] = unit_dosage
        if images:
            updated_values['images'] = images

        if updated_values:
            medicine.write(updated_values)

        return medicine


    # Delete Medicine
    def delete_medicine(self, medicine_id):
        """Delete the medicine from the system"""
        medicine = self.browse(medicine_id)
        if medicine:
            medicine_name = medicine.name
            medicine.unlink()

            # for stock in pharmacy.stocks:
            #     stock.unlink()

            medicine.message_post(body=f"Medicine {medicine_name} has been successfully deleted.")
            return True
        else:
            raise ValidationError("Medicine not found.")

    # Validation Methods for Fields
    def validate_name_fields(self, name):
        """Validate that the name is provided"""
        if not name:
            raise ValidationError("Name is required.")

    def validate_forme_fields(self, forme):
        """Validate that the forme is not too long or empty if provided"""
        if forme and len(forme) > 100:
            raise ValidationError("Forme should not exceed 100 characters.")

    def validate_presentation_fields(self, presentation):
        """Validate presentation if provided"""
        if presentation and len(presentation) > 100:
            raise ValidationError("Presentation should not exceed 100 characters.")

    def validate_composition_fields(self, composition):
        """Validate composition if provided"""
        if composition and len(composition) > 500:
            raise ValidationError("Composition should not exceed 500 characters.")

    def validate_dosage_fields(self, dosage):
        """Validate dosage if provided"""
        if dosage and len(dosage) > 100:
            raise ValidationError("Dosage should not exceed 100 characters.")

    def validate_unit_dosage_fields(self, unit_dosage):
        """Validate unit dosage if provided"""
        if unit_dosage and len(unit_dosage) > 50:
            raise ValidationError("Unit Dosage should not exceed 50 characters.")

    def validate_images_fields(self, images):
        """Validate images if provided"""
        if images:
            for image in images:
                if image.mimetype not in ['image/jpeg', 'image/png', 'image/gif']:
                    raise ValidationError("Only JPEG, PNG, and GIF images are allowed.")

    @api.model
    def _get_default_image(self):
        default_image = self.env['ir.attachment'].search([('name', '=', 'default_medicine_image')], limit=1)
        if not default_image:
            try:
                image_path = "../static/image/default_medicine_image.png"
                with open(image_path, 'rb') as image_file:
                    default_image_data = base64.b64encode(image_file.read()).decode(
                        'utf-8')
            except FileNotFoundError:
                raise ValidationError("The image file was not found at the specified path.")

            default_image = self.env['ir.attachment'].create({
                'name': 'default_medicine_image',
                'type': 'binary',
                'datas': default_image_data,
                'mimetype': 'image/png',
                'res_model': 'pharmacy.medicine',
                'res_id': 1,
            })
        return default_image.id