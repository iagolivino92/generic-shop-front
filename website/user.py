from flask_login import UserMixin


class _User:
    def __init__(self):
        self.id = None
        self.email = None
        self.last_name = None
        self.first_name = None
        self.role = None
        self.shop_id = None
        self.contact = None
        self.token = None
        self.is_authenticated = None
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def set_data(self, data):
        self.id = data.get('id')
        self.email = data.get('email')
        self.contact = data.get('contact')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.role = data.get('role')
        self.shop_id = data.get('shop_id')
