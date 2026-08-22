from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db
from app.models.user import User
from app.models.trip import Trip
from app.models.destination import Destination, Activity

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@admin_bp.route('/admin.html')
def dashboard():
    trips_count = Trip.query.count()
    active_users_count = User.query.filter_by(is_active=True).count()
    
    top_destination = Destination.query.order_by(Destination.trips_count.desc()).first()
    top_city_name = top_destination.name if top_destination else "Kyoto"
    top_city_trips = top_destination.trips_count if top_destination else 412
    
    all_trips = Trip.query.filter(Trip.total_budget > 0).all()
    avg_budget = round(sum(t.total_budget for t in all_trips) / max(1, len(all_trips)), 0) if all_trips else 2860
    
    users = User.query.order_by(User.created_at.desc()).all()
    popular_cities = Destination.query.order_by(Destination.trips_count.desc()).limit(10).all()
    popular_activities = Activity.query.order_by(Activity.bookings_count.desc()).limit(10).all()
    shared_count = Trip.query.filter_by(is_public=True).count()

    return render_template(
        'admin.html',
        trips_count=trips_count,
        active_users_count=active_users_count,
        top_city_name=top_city_name,
        top_city_trips=top_city_trips,
        avg_budget=int(avg_budget),
        users=users,
        popular_cities=popular_cities,
        popular_activities=popular_activities,
        shared_count=shared_count
    )


@admin_bp.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return redirect(url_for('admin.dashboard'))
