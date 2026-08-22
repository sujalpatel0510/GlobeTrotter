from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db
from app.models.user import User
from app.models.trip import Trip
from app.models.destination import Destination, Activity
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    # Platform overview statistics
    trips_count = Trip.query.count()
    active_users_count = User.query.filter_by(is_active=True).count()
    
    # Top destination by trips count
    top_destination = Destination.query.order_by(Destination.trips_count.desc()).first()
    top_city_name = top_destination.name if top_destination else "Kyoto"
    top_city_trips = top_destination.trips_count if top_destination else 412
    
    # Avg trip budget
    all_trips = Trip.query.filter(Trip.total_budget > 0).all()
    avg_budget = round(sum(t.total_budget for t in all_trips) / max(1, len(all_trips)), 0) if all_trips else 2860
    
    # All users
    users = User.query.order_by(User.created_at.desc()).all()
    
    # Popular cities and activities
    popular_cities = Destination.query.order_by(Destination.trips_count.desc()).limit(10).all()
    popular_activities = Activity.query.order_by(Activity.bookings_count.desc()).limit(10).all()
    
    # Shared itineraries count
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


@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot deactivate your own admin account.', 'error')
        return redirect(url_for('admin.dashboard'))
        
    user.is_active = not user.is_active
    db.session.commit()
    status_str = "activated" if user.is_active else "deactivated"
    flash(f"User {user.full_name} has been {status_str}.", "info")
    return redirect(url_for('admin.dashboard'))
