from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Owner(models.Model):
    _name = 'pharmacy.owner'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit to use message_post
    _description = 'Owner'

    user_id = fields.Many2one('res.users', string='Owner user', ondelete='set null')
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    password = fields.Char(string='Password', required=True)
    carte_id = fields.Char(string='Carte ID')
    address = fields.Char(string='Address')
    phone = fields.Char(string='Phone')
    is_verified = fields.Boolean(string="Is Verified", default=False)

    # Relation: One owner can have only one pharmacy
    pharmacy_id = fields.One2many('pharmacy.pharmacy', 'owner_id', string='Pharmacy', limit=1)

    @api.model
    def create_owner(self, name, email, password):
        """Create an owner with basic information and send a verification email"""
        self.validate_name_fields(name)
        self.validate_email_fields(email)
        self.validate_password_fields(password)

        user_vals = {
            'name': name,
            'login': email,  # Use the email as the login for authentication
            'password': password,  # Assign password for login
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],  # Assign the user to the general user group
        }
        user = self.env['res.users'].create(user_vals)

        # Create the Owner record and link it to the user
        owner = self.create({
            'name': name,
            'email': email,
            'password': password,
            'user_id': user.id,  # Link to the user account
        })

        owner.message_post(body=f"Owner {owner.name} created successfully. Please verify your email to complete registration.")
        return owner

    def update_owner(self, owner_id, name=None, email=None, password=None, carte_id=None, address=None, phone=None):
        """Update the owner's details and validate required fields"""
        owner = self.browse(owner_id)

        if not owner:
            raise ValidationError("Owner not found.")

        if name:
            self.validate_name_fields(name)
        if email:
            self.validate_email_fields(email)
        if password:
            self.validate_password_fields(password)
        if phone:
            self.validate_phone_fields(phone)
        if address:
            self.validate_address_fields(address)
        if carte_id:
            self.validate_carte_id_fields(carte_id)

        updated_values = {}
        if name:
            updated_values['name'] = name
        if email:
            updated_values['email'] = email
        if password:
            updated_values['password'] = password
        if carte_id:
            updated_values['carte_id'] = carte_id
        if address:
            updated_values['address'] = address
        if phone:
            updated_values['phone'] = phone

        if email or password:
            user = owner.user_id
            if user:
                user_vals = {}
                if email:
                    user_vals['login'] = email
                if password:
                    user_vals['password'] = password
                if user_vals:
                    user.write(user_vals)

        if updated_values:
            owner.write(updated_values)

        owner.message_post(body=f"Owner {owner.name} updated successfully.")
        return owner

    def delete_owner(self, owner_id):
        """Delete the owner from the system"""
        owner = self.browse(owner_id)
        if owner:
            user = owner.user_id  # Get the associated user

            if user:
                user.unlink()

            owner.unlink()

            owner.message_post(body=f"Owner {owner.name} has been successfully deleted.")
            return True
        else:
            raise ValidationError("Owner not found.")

    # Validation Methods (unchanged)
    def validate_name_fields(self, name):
        if not name:
            raise ValidationError("Name is required.")

    def validate_password_fields(self, password):
        if not password:
            raise ValidationError("Password is required.")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    def validate_email_fields(self, email):
        if not email:
            raise ValidationError("Email is required.")

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format.")

    def validate_carte_id_fields(self, carte_id):
        if not carte_id:
            raise ValidationError("Carte ID is required.")

    def validate_address_fields(self, address):
        if not address:
            raise ValidationError("Address is required.")

    def validate_phone_fields(self, phone):
        if not phone:
            raise ValidationError("Phone is required.")

        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")

        if len(phone) < 10 or len(phone) > 15:
            raise ValidationError("Phone number must be between 10 and 15 digits.")

    # Commented out since we don't need email verification now
    # def send_verification_email(self, owner):
    #     """Send verification email to the owner"""
    #     verification_link = f"http://yourdomain.com/verify?owner_id={owner.id}"
    #     message = f"Dear {owner.name},\n\nPlease click the link below to verify your email:\n{verification_link}"

    #     owner_message = self.env['mail.mail'].create({
    #         'subject': 'Email Verification',
    #         'body_html': message,
    #         'email_to': owner.email,
    #     })
    #     owner_message.send()

    # def verify_owner(self, owner_id):
    #     """ Function to verify the owner when they click on the verification link """
    #     owner = self.browse(owner_id)
    #     if owner:
    #         owner.is_verified = True
    #         # Redirect the user to the profile completion page
    #         self.redirect_to_profile_completion(owner)

    # def redirect_to_profile_completion(self, owner):
    #     """ Redirect the owner to complete their profile """
    #     # Here you can write code to redirect the user to the profile completion page
    #     # In the real application, you will use routing in the frontend
    #     # For simplicity, we will just set a flag
    #     owner.message_post(body="Verification successful. Please complete your profile.")
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'pharmacy.owner',
    #         'view_mode': 'form',
    #         'res_id': owner.id,
    #         'target': 'new',  # Open the form in a new window or view
    #     }
    #
    # def check_required_information(self):
    #     """ Check if all required fields are filled in after the owner submits their information """
    #     for owner in self:
    #         if owner.is_verified:
    #             # Check if required fields are filled
    #             if not owner.carte_id or not owner.address or not owner.phone:
    #                 raise ValidationError("Carte ID, Address, and Phone are required to complete your profile.")
    #             else:
    #                 # Profile is complete
    #                 owner.message_post(body="Profile completed successfully!")
    #                 return True