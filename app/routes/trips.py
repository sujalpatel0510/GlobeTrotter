from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import db
from app.models.trip import Trip
from app.models.itinerary import ItinerarySection, ItineraryItem
from app.models.destination import Destination, Activity
from app.utils.helpers import save_uploaded_image

trips_bp = Blueprint('trips', __name__)


@trips_bp.route('/trips')
@trips_bp.route('/my-trips')
@trips_bp.route('/my-trips.html')
def my_trips():
    search_query = request.args.get('q', '').strip().lower()
    user_id = current_user.id if current_user.is_authenticated else 1
    
    query = Trip.query.filter_by(user_id=user_id)
    if search_query:
        query = query.filter(Trip.name.ilike(f'%{search_query}%') | Trip.description.ilike(f'%{search_query}%'))
        
    all_trips = query.order_by(Trip.start_date.desc()).all()
    
    ongoing_trips = [t for t in all_trips if t.status == 'ongoing']
    upcoming_trips = [t for t in all_trips if t.status == 'upcoming']
    completed_trips = [t for t in all_trips if t.status == 'completed']
    draft_trips = [t for t in all_trips if t.status == 'draft']
    
    return render_template(
        'my-trips.html',
        ongoing_trips=ongoing_trips,
        upcoming_trips=upcoming_trips,
        completed_trips=completed_trips,
        draft_trips=draft_trips,
        total_count=len(all_trips),
        search_query=search_query
    )


@trips_bp.route('/trips/create', methods=['GET', 'POST'])
@trips_bp.route('/create-trip.html', methods=['GET', 'POST'])
def create_trip():
    if request.method == 'POST':
        trip_name = request.form.get('trip_name') or request.form.get('trip-name', '').strip()
        start_date_str = request.form.get('start_date') or request.form.get('start-date', '').strip()
        end_date_str = request.form.get('end_date') or request.form.get('end-date', '').strip()
        start_place = request.form.get('start_place') or request.form.get('select-place', '').strip()
        description = request.form.get('description') or request.form.get('trip-desc', '').strip()
        total_budget_str = request.form.get('total_budget', '3000').strip()

        if not trip_name:
            flash('Please enter a name for your trip.', 'error')
            return redirect(url_for('trips.create_trip'))

        start_date = None
        end_date = None
        try:
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass

        try:
            total_budget = float(total_budget_str) if total_budget_str else 3000.0
        except ValueError:
            total_budget = 3000.0

        cover_image = None
        if 'cover_photo' in request.files:
            file = request.files['cover_photo']
            cover_image = save_uploaded_image(file, subfolder='trips')

        status = 'draft'
        today = datetime.utcnow().date()
        if start_date and end_date:
            if start_date <= today <= end_date:
                status = 'ongoing'
            elif start_date > today:
                status = 'upcoming'
            else:
                status = 'completed'

        user_id = current_user.id if current_user.is_authenticated else 1
        new_trip = Trip(
            user_id=user_id,
            name=trip_name,
            start_date=start_date,
            end_date=end_date,
            start_place=start_place,
            description=description,
            total_budget=total_budget,
            cover_image=cover_image,
            status=status
        )

        db.session.add(new_trip)
        db.session.flush()

        default_section = ItinerarySection(
            trip_id=new_trip.id,
            section_order=1,
            title=start_place if start_place else f"{trip_name} - Stop 1",
            description="Initial trip stop.",
            start_date=start_date,
            end_date=end_date,
            allocated_budget=round(total_budget * 0.5, 2)
        )
        db.session.add(default_section)
        db.session.commit()

        return redirect(url_for('itinerary.itinerary_builder', trip_id=new_trip.id))

    suggested_places = Destination.query.limit(6).all()
    suggested_activities = Activity.query.limit(8).all()

    return render_template(
        'create-trip.html',
        suggested_places=suggested_places,
        suggested_activities=suggested_activities
    )


@trips_bp.route('/trips/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    db.session.delete(trip)
    db.session.commit()
    return redirect(url_for('trips.my_trips'))


@trips_bp.route('/trips/<int:trip_id>/duplicate', methods=['POST', 'GET'])
def duplicate_trip(trip_id):
    original_trip = Trip.query.get_or_404(trip_id)
    user_id = current_user.id if current_user.is_authenticated else 1

    new_trip = Trip(
        user_id=user_id,
        name=f"Copy of {original_trip.name}",
        start_date=original_trip.start_date,
        end_date=original_trip.end_date,
        start_place=original_trip.start_place,
        description=original_trip.description,
        total_budget=original_trip.total_budget,
        status='draft'
    )
    db.session.add(new_trip)
    db.session.flush()

    for orig_sec in original_trip.sections:
        new_sec = ItinerarySection(
            trip_id=new_trip.id,
            section_order=orig_sec.section_order,
            title=orig_sec.title,
            description=orig_sec.description,
            start_date=orig_sec.start_date,
            end_date=orig_sec.end_date,
            allocated_budget=orig_sec.allocated_budget
        )
        db.session.add(new_sec)
        db.session.flush()

        for orig_item in orig_sec.items:
            new_item = ItineraryItem(
                section_id=new_sec.id,
                title=orig_item.title,
                description=orig_item.description,
                time_label=orig_item.time_label,
                category=orig_item.category,
                cost=orig_item.cost,
                order_index=orig_item.order_index,
                day_number=orig_item.day_number
            )
            db.session.add(new_item)

    db.session.commit()
    return redirect(url_for('itinerary.itinerary_view', trip_id=new_trip.id))
