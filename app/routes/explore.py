from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db
from app.models.destination import Destination, Activity
from app.models.trip import Trip
from app.models.itinerary import ItinerarySection, ItineraryItem

explore_bp = Blueprint('explore', __name__)


@explore_bp.route('/explore')
@explore_bp.route('/search.html')
def search():
    query = request.args.get('q', '').strip()
    active_tab = request.args.get('tab', 'activities')
    
    act_query = Activity.query
    dest_query = Destination.query
    
    if query:
        act_query = act_query.filter(
            Activity.name.ilike(f'%{query}%') |
            Activity.category.ilike(f'%{query}%') |
            Activity.description.ilike(f'%{query}%')
        )
        dest_query = dest_query.filter(
            Destination.name.ilike(f'%{query}%') |
            Destination.country.ilike(f'%{query}%') |
            Destination.description.ilike(f'%{query}%')
        )
        
    activities = act_query.all()
    destinations = dest_query.all()
    
    user_id = current_user.id if current_user.is_authenticated else 1
    user_trips = Trip.query.filter_by(user_id=user_id).all()

    return render_template(
        'search.html',
        query=query,
        active_tab=active_tab,
        activities=activities,
        destinations=destinations,
        user_trips=user_trips
    )


@explore_bp.route('/explore/add-activity', methods=['POST'])
def add_activity():
    activity_id = request.form.get('activity_id', type=int)
    trip_id = request.form.get('trip_id', type=int)
    
    if not activity_id or not trip_id:
        return redirect(url_for('explore.search'))
        
    activity = Activity.query.get_or_404(activity_id)
    trip = Trip.query.get_or_404(trip_id)
    
    section = trip.sections.first()
    if not section:
        section = ItinerarySection(
            trip_id=trip.id,
            section_order=1,
            title=activity.destination.name if activity.destination else "Trip Stops",
            allocated_budget=round(trip.total_budget * 0.5, 2)
        )
        db.session.add(section)
        db.session.flush()
        
    cat_lower = activity.category.lower()
    if 'food' in cat_lower or 'drink' in cat_lower:
        item_cat = 'meals'
    elif 'stay' in cat_lower or 'hotel' in cat_lower:
        item_cat = 'stay'
    elif 'transfer' in cat_lower or 'flight' in cat_lower:
        item_cat = 'transport'
    else:
        item_cat = 'activities'
        
    new_item = ItineraryItem(
        section_id=section.id,
        title=activity.name,
        description=f"{activity.category} · {activity.duration or 'Flexible'}",
        time_label="Flexible",
        category=item_cat,
        cost=activity.price,
        order_index=section.items.count() + 1,
        day_number=1
    )
    
    db.session.add(new_item)
    activity.bookings_count = (activity.bookings_count or 0) + 1
    db.session.commit()
    
    return redirect(url_for('itinerary.itinerary_view', trip_id=trip.id))


@explore_bp.route('/explore/add-city', methods=['POST'])
def add_city():
    destination_id = request.form.get('destination_id', type=int)
    trip_id = request.form.get('trip_id', type=int)
    
    if not destination_id or not trip_id:
        return redirect(url_for('explore.search'))
        
    dest = Destination.query.get_or_404(destination_id)
    trip = Trip.query.get_or_404(trip_id)
    
    new_section = ItinerarySection(
        trip_id=trip.id,
        section_order=trip.sections.count() + 1,
        title=f"{dest.name}, {dest.country}",
        description=dest.description or f"Exploring {dest.name}",
        allocated_budget=500.0
    )
    db.session.add(new_section)
    dest.trips_count = (dest.trips_count or 0) + 1
    db.session.commit()
    
    return redirect(url_for('itinerary.itinerary_builder', trip_id=trip.id))
