from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Explicitly import all models for metadata discovery and table creation
from app.models.user import User
from app.models.trip import Trip
from app.models.itinerary import ItinerarySection, ItineraryItem
from app.models.destination import Destination, Activity
from app.models.community import CommunityPost
