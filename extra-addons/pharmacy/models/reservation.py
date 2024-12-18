from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Reservation(models.Model):
    _name = 'pharmacy.reservation'
    _description = 'Reservation'

    message = fields.Text(string='Message')
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    price = fields.Float(string='Price', required=True)

    state = fields.Selection([
        ('wait', 'Wait'),
        ('available', 'Available'),
        ('not_available', 'Not Available')
    ], string='State', default='wait')

    client_id = fields.Many2one('pharmacy.client', string='Client', required=True, ondelete='cascade')
    stock_id = fields.Many2one('pharmacy.stock', string='Stock', required=True, ondelete='cascade')

    @api.model
    def create_reservation(self, client_id, stock_id, quantity=1, price=0.0, message=None):
        """Create a reservation and validate required fields"""
        # Validate required fields
        self.validate_reservation_fields(quantity, price, client_id, stock_id)

        # Create the reservation record
        reservation = self.create({
            'client_id': client_id,
            'stock_id': stock_id,
            'quantity': quantity,
            'price': price,
            'message': message
        })

        reservation.message_post(body="Reservation created successfully.")
        return reservation

    def update_reservation(self, reservation_id, quantity=None, price=None, state=None, message=None):
        """Update the reservation details and validate fields"""
        reservation = self.browse(reservation_id)

        if not reservation:
            raise ValidationError("Reservation not found.")

        if quantity is not None or price is not None or reservation.client_id.id is not None or reservation.stock_id.id is not None:
            self.validate_reservation_fields(quantity, price, reservation.client_id.id, reservation.stock_id.id)

        updated_values = {}
        if quantity:
            updated_values['quantity'] = quantity
        if price:
            updated_values['price'] = price
        if state:
            updated_values['state'] = state
        if message:
            updated_values['message'] = message

        if updated_values:
            reservation.write(updated_values)

        return reservation

    def delete_reservation(self, reservation_id):
        """Delete the reservation"""
        reservation = self.browse(reservation_id)
        if reservation:
            reservation_name = reservation.message if reservation.message else "Reservation"
            reservation.unlink()
            reservation.message_post(body=f"Reservation {reservation_name} has been successfully deleted.")
            return True
        else:
            raise ValidationError("Reservation not found.")

    def validate_reservation_fields(self, quantity, price, client_id, stock_id):
        """Validate that the required fields are provided for a reservation"""
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        if not client_id:
            raise ValidationError("Client is required.")
        if not stock_id:
            raise ValidationError("Stock is required.")