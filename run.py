import os
import sys
from app import create_app
from app.models import db
from app.seeder import seed_database

app = create_app(os.environ.get('FLASK_ENV', 'development'))


def initialize_environment():
    with app.app_context():
        try:
            db.create_all()
            # If database is completely empty, auto-seed demo data for immediate testing
            from app.models.user import User
            if not User.query.first():
                seed_database()
        except Exception as e:
            app.logger.warning(f"Database initialization notice: {e}")


if __name__ == '__main__':
    # Check CLI arguments
    if '--init-db' in sys.argv:
        with app.app_context():
            db.create_all()
            print("Database initialized.")
            if '--seed' in sys.argv or True:
                seed_database()
        if len(sys.argv) == 2 or (len(sys.argv) == 3 and '--seed' in sys.argv):
            sys.exit(0)

    # Initialize environment tables and seed if empty
    initialize_environment()

    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=True)
else:
    # When running under Gunicorn
    initialize_environment()
