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
            from app.models.user import User
            if not User.query.first():
                seed_database()
            print("[PostgreSQL] Connected and verified schema.")
        except Exception as e:
            print(f"[PostgreSQL Error] Database initialization failed: {e}")
            raise e


if __name__ == '__main__':
    if '--init-db' in sys.argv:
        initialize_environment()
        print("[PostgreSQL] Database initialized and seeded successfully.")
        if len(sys.argv) <= 3:
            sys.exit(0)

    initialize_environment()

    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    print(f"Starting GlobeTrotter Flask application on http://localhost:{port}")
    app.run(host=host, port=port, debug=True)
else:
    initialize_environment()
