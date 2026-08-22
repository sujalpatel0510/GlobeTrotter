import os
from pathlib import Path
from flask import Flask, send_from_directory, render_template, jsonify
from app.config import config_by_name, BASE_DIR
from app.models import db, login_manager, migrate
from app.routes import (
    auth_bp,
    main_bp,
    trips_bp,
    itinerary_bp,
    explore_bp,
    community_bp,
    profile_bp,
    admin_bp,
    api_bp
)


def create_app(config_name=None):
    """Application factory for GlobeTrotter Flask application using user templates."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / 'templates'),
        static_folder=str(BASE_DIR / 'templates'),
        static_url_path=''
    )

    # Load configuration
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'avatars'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'trips'), exist_ok=True)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(itinerary_bp)
    app.register_blueprint(explore_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Static routes
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(BASE_DIR / 'templates' / 'css', filename)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(BASE_DIR / 'templates' / 'js', filename)

    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/base.html')
    def serve_base():
        return render_template('base.html')

    # Custom Jinja filters
    @app.template_filter('currency')
    def currency_filter(value):
        try:
            return f"${float(value):,.0f}"
        except (ValueError, TypeError):
            return "$0"

    @app.template_filter('date_format')
    def date_format_filter(value, format='%b %d, %Y'):
        if not value:
            return ''
        return value.strftime(format)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('base.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('base.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('base.html'), 500

    # Register CLI commands
    @app.cli.command('init-db')
    def init_db_command():
        """Initialize database tables."""
        db.create_all()
        print("Database tables initialized.")

    @app.cli.command('seed-db')
    def seed_db_command():
        """Seed database with demo data."""
        from app.seeder import seed_database
        db.create_all()
        seed_database()

    return app
