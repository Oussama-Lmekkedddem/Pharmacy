from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

class Reservation(models.Model):
    _name = 'pharmacy.reservation'
    _description = 'Reservation'

    message = fields.Text(string='Message')
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    price = fields.Float(string='Price', required=True)

    state = fields.Selection([
        ('wait', 'Wait'),
        ('finalized', 'Finalized'),
        ('canceled', 'Canceled')
    ], string='State', default='wait')

    cancel_date = fields.Datetime(string="Cancellation Date")
    finalized_date = fields.Datetime(string="Finalization Date")

    client_id = fields.Many2one('pharmacy.client', string='Client', required=True, ondelete='cascade')
    stock_id = fields.Many2one('pharmacy.stock', string='Stock', required=True, ondelete='cascade')


    # invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    #
    # @api.model
    # def create(self, vals):
    #     _logger.info("Starting reservation creation...")
    #     reservation = super(Reservation, self).create(vals)
    #     _logger.info(f"Reservation {reservation.id} created. Attempting to create invoice.")
    #     reservation._create_invoice()
    #     _logger.info(f"Invoice for reservation {reservation.id} created. Attempting to send email.")
    #     reservation._send_reservation_email()
    #     _logger.info(f"Email for reservation {reservation.id} sent.")
    #     return reservation
    #
    # def _create_invoice(self):
    #     _logger.info(f"Starting invoice creation for reservation {self.id}...")
    #     try:
    #         # Log client and stock details
    #         _logger.info(f"Client ID: {self.client_id.id}, Stock ID: {self.stock_id.id}")
    #
    #         # Prepare invoice values
    #         invoice_vals = {
    #             'move_type': 'out_invoice',  # Sales invoice
    #             'partner_id': self.client_id.id,  # Client (must be valid)
    #             'invoice_date': fields.Date.today(),  # Today's date
    #             'invoice_line_ids': [(0, 0, {
    #                 'name': f"Reservation for {self.stock_id.medicine_id.name}",  # Medicine name
    #                 'quantity': self.quantity,  # Quantity
    #                 'price_unit': self.price / self.quantity if self.quantity else 0.0,  # Unit price
    #             })],
    #         }
    #         _logger.info(f"Invoice values: {invoice_vals}")
    #
    #         # Create and post the invoice
    #         invoice = self.env['account.move'].create(invoice_vals)
    #         self.invoice_id = invoice.id
    #         invoice.action_post()
    #         _logger.info(f"Invoice {invoice.id} created and posted successfully.")
    #     except Exception as e:
    #         _logger.error(f"Error creating invoice for reservation {self.id}: {str(e)}")
    #
    # def _send_reservation_email(self):
    #     _logger.info(f"Attempting to send email for reservation {self.id}...")
    #     template = self.env.ref('pharmacy.email_template_reservation_invoice')
    #     if template:
    #         try:
    #             template.sudo().send_mail(self.id, force_send=True)
    #             _logger.info(f"Email sent successfully for reservation {self.id}.")
    #         except Exception as e:
    #             _logger.error(f"Failed to send email for reservation {self.id}: {str(e)}")

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

    def delete_old_reservations(self):
        """Delete reservations that are finalized or canceled for more than 3 days"""
        now = datetime.now()
        three_days_ago = now - timedelta(days=3)

        old_reservations = self.sudo().search([
            '|',
            ('state', '=', 'canceled'),
            ('state', '=', 'finalized'),
            '|',
            ('cancel_date', '<=', three_days_ago),
            ('finalized_date', '<=', three_days_ago)
        ])

        for reservation in old_reservations:
            self.delete_reservation(reservation.id)

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