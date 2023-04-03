from website import create_app
from website.utils import create_admin_instance

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        create_admin_instance()
    app.run(debug=True)
