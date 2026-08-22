from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from app.models import db
from app.models.trip import Trip
from app.models.itinerary import ItinerarySection, ItineraryItem

itinerary_bp = Blueprint('itinerary', __name__, url_prefix='/trips')


@itinerary_bp.route('/<int:trip_id>')
def itinerary_view(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    # Check view permissions: owner, admin, or public
    if not trip.is_public and (not current_user.is_authenticated or (trip.user_id != current_user.id and not current_user.is_admin)):
        flash('This trip is private. Please log in with an authorized account.', 'warning')
        return redirect(url_for('auth.login'))

    # Group items by day_number
    sections = trip.sections.all()
    days_dict = {}
    
    for section in sections:
        for item in section.items:
            day = item.day_number or 1
            if day not in days_dict:
                days_dict[day] = []
            days_dict[day].append(item)
            
    # Sort days
    sorted_days = sorted(days_dict.items(), key=lambda x: x[0])

    return render_template(
        'itinerary-view.html',
        trip=trip,
        sections=sections,
        sorted_days=sorted_days,
        breakdown=trip.budget_breakdown,
        is_owner=(current_user.is_authenticated and trip.user_id == current_user.id)
    )


@itinerary_bp.route('/<int:trip_id>/builder', methods=['GET', 'POST'])
@login_required
def itinerary_builder(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        # Process updated sections from form or builder save
        section_titles = request.form.getlist('section_title[]')
        section_descriptions = request.form.getlist('section_description[]')
        section_dates = request.form.getlist('section_date_range[]')
        section_budgets = request.form.getlist('section_budget[]')

        if section_titles:
            # Delete old sections and re-create updated ones
            ItinerarySection.query.filter_by(trip_id=trip.id).delete()
            
            for i, title in enumerate(section_titles):
                if not title.strip():
                    continue
                
                desc = section_descriptions[i] if i < len(section_descriptions) else ''
                date_str = section_dates[i] if i < len(section_dates) else ''
                budget_raw = section_budgets[i].replace('$', '').replace(',', '').strip() if i < len(section_budgets) else '0'
                try:
                    budget = float(budget_raw)
                except ValueError:
                    budget = 0.0

                sec = ItinerarySection(
                    trip_id=trip.id,
                    section_order=i + 1,
                    title=title.strip(),
                    description=desc.strip(),
                    date_range_text=date_str.strip(),
                    allocated_budget=budget
                )
                db.session.add(sec)

            db.session.commit()
            flash('Itinerary sections updated successfully!', 'success')
            return redirect(url_for('itinerary.itinerary_view', trip_id=trip.id))

    sections = trip.sections.all()
    return render_template(
        'itinerary-builder.html',
        trip=trip,
        sections=sections
    )


@itinerary_bp.route('/share/<share_token>')
def shared_itinerary(share_token):
    trip = Trip.query.filter_by(share_token=share_token).first_or_404()
    
    sections = trip.sections.all()
    days_dict = {}
    for section in sections:
        for item in section.items:
            day = item.day_number or 1
            if day not in days_dict:
                days_dict[day] = []
            days_dict[day].append(item)
            
    sorted_days = sorted(days_dict.items(), key=lambda x: x[0])

    return render_template(
        'shared-itinerary.html',
        trip=trip,
        sections=sections,
        sorted_days=sorted_days,
        breakdown=trip.budget_breakdown
    )
