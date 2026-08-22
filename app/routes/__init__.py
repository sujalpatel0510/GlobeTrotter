from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.trips import trips_bp
from app.routes.itinerary import itinerary_bp
from app.routes.explore import explore_bp
from app.routes.community import community_bp
from app.routes.profile import profile_bp
from app.routes.admin import admin_bp
from app.routes.api import api_bp

__all__ = [
    'auth_bp',
    'main_bp',
    'trips_bp',
    'itinerary_bp',
    'explore_bp',
    'community_bp',
    'profile_bp',
    'admin_bp',
    'api_bp'
]
