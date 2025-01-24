import base64
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ImportMedicineWizard(models.TransientModel):
    _name = 'import.medicine.wizard'
    _description = 'Import Medicines Wizard'

    file = fields.Binary(string="File", required=True)
    file_name = fields.Char(string="File Name", required=True)

    def import_medicines(self):
        if not self.file:
            raise ValidationError("Please upload a file.")

        file_content = base64.b64decode(self.file)
        try:
            import pandas as pd
            import io
            df = pd.read_excel(io.BytesIO(file_content))

            # Check for required columns
            required_columns = ['name', 'forme', 'presentation', 'composition', 'dosage', 'unit_dosage']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValidationError(f"The file must contain the following columns: {', '.join(required_columns)}. "
                                      f"Missing columns: {', '.join(missing_columns)}")

            # Iterate through rows and create medicines
            for _, row in df.iterrows():
                self.env['pharmacy.medicine'].create({
                    'name': row['name'],
                    'forme': row['forme'],
                    'presentation': row['presentation'],
                    'composition': row['composition'],
                    'dosage': row['dosage'],
                    'unit_dosage': row['unit_dosage'],
                })

        except Exception as e:
            raise ValidationError(f"Error processing the file: {e}")

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
