class ForeignUser:
    def __init__(self):
        self.email = None

    def get_email(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def set_data(self, data):
        self.email = data.get('email')
