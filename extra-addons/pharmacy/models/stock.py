from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Stock(models.Model):
    _name = 'pharmacy.stock'
    _description = 'Stock'

    price = fields.Float(string='Price', required=True)
    quantity = fields.Integer(string='Quantity', required=True)

    reservations = fields.One2many('pharmacy.reservation', 'stock_id', string='Reservations')

    pharmacy_id = fields.Many2one(
        'pharmacy.pharmacy',
        string='Pharmacy',
        required=True,
        ondelete='cascade',
        index=True
    )

    medicine_id = fields.Many2one(
        'pharmacy.medicine',
        string='Medicine',
        required=True,
        ondelete='cascade',
        index=True
    )

    @api.model
    def create_stock(self, pharmacy_id, medicine_id, price, quantity):
        """Create a stock and validate required fields"""
        # Validate required fields
        self.validate_stock_fields(price, quantity, pharmacy_id, medicine_id)

        # Create the stock record
        stock = self.create({
            'pharmacy_id': pharmacy_id,
            'medicine_id': medicine_id,
            'price': price,
            'quantity': quantity,
        })

        stock.message_post(body="Stock created successfully.")
        return stock

    def update_stock(self, stock_id, price=None, quantity=None):
        """Update the stock's details and validate fields"""
        stock = self.browse(stock_id)

        if not stock:
            raise ValidationError("Stock not found.")

        # Validate fields before updating
        if price is not None or quantity is not None:
            self.validate_stock_fields(price, quantity, stock.pharmacy_id.id, stock.medicine_id.id)

        # Proceed with updating the fields
        updated_values = {}
        if price is not None:
            updated_values['price'] = price
        if quantity is not None:
            updated_values['quantity'] = quantity

        if updated_values:
            stock.write(updated_values)

        return stock

    def delete_stock(self, stock_id):
        """Delete the stock"""
        stock = self.browse(stock_id)
        if stock:
            stock_name = stock.medicine_id.name if stock.medicine_id else "Stock"
            stock.unlink()

            stock.message_post(body=f"Stock {stock_name} has been successfully deleted.")
            return True
        else:
            raise ValidationError("Stock not found.")

    def validate_stock_fields(self, price, quantity, pharmacy_id, medicine_id):
        """Validate that the required fields are provided for a stock"""
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        if not pharmacy_id:
            raise ValidationError("Pharmacy is required.")
        if not medicine_id:
            raise ValidationError("Medicine is required.")
