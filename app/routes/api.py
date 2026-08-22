from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db
from app.models.trip import Trip
from app.models.itinerary import ItinerarySection, ItineraryItem
from app.models.destination import Destination, Activity

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/trips/<int:trip_id>/toggle-share', methods=['POST'])
@login_required
def toggle_share(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    trip.is_public = not trip.is_public
    db.session.commit()
    return jsonify({
        'success': True,
        'is_public': trip.is_public,
        'share_token': trip.share_token,
        'share_url': f"/trips/share/{trip.share_token}"
    })


@api_bp.route('/trips/<int:trip_id>/sections', methods=['POST'])
@login_required
def add_section(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}
    title = data.get('title', f"Section {trip.sections.count() + 1}")
    description = data.get('description', '')
    budget = float(data.get('allocated_budget', 0.0))
    date_range = data.get('date_range', '')

    new_section = ItinerarySection(
        trip_id=trip.id,
        section_order=trip.sections.count() + 1,
        title=title,
        description=description,
        date_range_text=date_range,
        allocated_budget=budget
    )
    db.session.add(new_section)
    db.session.commit()

    return jsonify({'success': True, 'section': new_section.to_dict()}), 201


@api_bp.route('/sections/<int:section_id>', methods=['DELETE'])
@login_required
def delete_section(section_id):
    section = ItinerarySection.query.get_or_404(section_id)
    if section.trip.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(section)
    db.session.commit()
    return jsonify({'success': True})


@api_bp.route('/sections/<int:section_id>/items', methods=['POST'])
@login_required
def add_item(section_id):
    section = ItinerarySection.query.get_or_404(section_id)
    if section.trip.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}
    title = data.get('title', 'New Activity')
    description = data.get('description', '')
    time_label = data.get('time_label', 'Flexible')
    category = data.get('category', 'activities')
    cost = float(data.get('cost', 0.0))
    day_number = int(data.get('day_number', 1))

    item = ItineraryItem(
        section_id=section.id,
        title=title,
        description=description,
        time_label=time_label,
        category=category,
        cost=cost,
        day_number=day_number,
        order_index=section.items.count() + 1
    )
    db.session.add(item)
    db.session.commit()

    return jsonify({'success': True, 'item': item.to_dict()}), 201


@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = ItineraryItem.query.get_or_404(item_id)
    if item.section.trip.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})


@api_bp.route('/search')
def api_search():
    query = request.args.get('q', '').strip()
    destinations = Destination.query
    activities = Activity.query
    
    if query:
        destinations = destinations.filter(Destination.name.ilike(f'%{query}%'))
        activities = activities.filter(Activity.name.ilike(f'%{query}%'))
        
    return jsonify({
        'destinations': [d.to_dict() for d in destinations.limit(10).all()],
        'activities': [a.to_dict() for a in activities.limit(10).all()]
    })
