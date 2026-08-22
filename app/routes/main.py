import calendar as py_calendar
from datetime import datetime, date
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import db
from app.models.user import User
from app.models.trip import Trip
from app.models.destination import Destination

main_bp = Blueprint('main', __name__)


@main_bp.route('/dashboard')
@main_bp.route('/dashboard.html')
def dashboard():
    user = current_user if current_user.is_authenticated else User.query.filter_by(email='maya@example.com').first()
    user_id = user.id if user else 1
    
    user_trips = Trip.query.filter_by(user_id=user_id).order_by(Trip.created_at.desc()).all()
    
    upcoming_trips = [t for t in user_trips if t.status == 'upcoming']
    ongoing_trips = [t for t in user_trips if t.status == 'ongoing']
    draft_trips = [t for t in user_trips if t.status == 'draft']
    completed_trips = [t for t in user_trips if t.status == 'completed']
    budget_trips = [t for t in user_trips if t.total_budget > 0][:3]
    featured_destinations = Destination.query.order_by(Destination.trips_count.desc()).limit(4).all()
    
    return render_template(
        'dashboard.html',
        upcoming_trips=upcoming_trips,
        ongoing_trips=ongoing_trips,
        draft_trips=draft_trips,
        completed_trips=completed_trips,
        budget_trips=budget_trips,
        featured_destinations=featured_destinations,
        total_trips_count=len(user_trips),
        user=user
    )


@main_bp.route('/calendar')
@main_bp.route('/calendar.html')
def calendar_view():
    year = request.args.get('year', 2026, type=int)
    month = request.args.get('month', 1, type=int)
    
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    month_name = py_calendar.month_name[month]
    cal = py_calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)
    
    user_id = current_user.id if current_user.is_authenticated else 1
    user_trips = Trip.query.filter_by(user_id=user_id).all()
    
    events_by_day = {}
    for trip in user_trips:
        if trip.start_date and trip.end_date:
            cur = trip.start_date
            while cur <= trip.end_date:
                if cur.year == year and cur.month == month:
                    day = cur.day
                    if day not in events_by_day:
                        events_by_day[day] = []
                    events_by_day[day].append({
                        'trip_id': trip.id,
                        'name': trip.name,
                        'status': trip.status,
                        'color_class': 'gold' if trip.status == 'ongoing' else ('coral' if trip.status == 'upcoming' else 'teal')
                    })
                if cur == trip.end_date:
                    break
                try:
                    from datetime import timedelta
                    cur += timedelta(days=1)
                except Exception:
                    break

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render_template(
        'calendar.html',
        year=year,
        month=month,
        month_name=month_name,
        month_days=month_days,
        events_by_day=events_by_day,
        prev_month=prev_month,
        prev_year=prev_year,
        next_month=next_month,
        next_year=next_year,
        trips=user_trips
    )


@main_bp.route('/health')
def health():
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    })
