from datetime import datetime
from app.models import db


class ItinerarySection(db.Model):
    __tablename__ = 'itinerary_sections'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    section_order = db.Column(db.Integer, default=1)
    title = db.Column(db.String(150), nullable=False)  # e.g., "Hanoi, Vietnam"
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    date_range_text = db.Column(db.String(100), nullable=True)  # e.g. "Jun 10 → Jun 13"
    allocated_budget = db.Column(db.Float, default=0.0)

    # Relationships
    items = db.relationship('ItineraryItem', backref='section', cascade='all, delete-orphan',
                            order_by='ItineraryItem.order_index', lazy='dynamic')

    @property
    def total_spent(self):
        return round(sum(item.cost or 0.0 for item in self.items), 2)

    @property
    def formatted_date_range(self):
        if self.date_range_text:
            return self.date_range_text
        if self.start_date and self.end_date:
            return f"{self.start_date.strftime('%b %d')} → {self.end_date.strftime('%b %d')}"
        return "Dates pending"

    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'section_order': self.section_order,
            'title': self.title,
            'description': self.description,
            'date_range': self.formatted_date_range,
            'allocated_budget': self.allocated_budget,
            'total_spent': self.total_spent,
            'items': [item.to_dict() for item in self.items]
        }

    def __repr__(self):
        return f"<ItinerarySection {self.title}>"


class ItineraryItem(db.Model):
    __tablename__ = 'itinerary_items'

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('itinerary_sections.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)  # e.g. "Arrive Tokyo Narita"
    description = db.Column(db.Text, nullable=True)     # e.g. "Airport transfer to Shinjuku hotel"
    time_label = db.Column(db.String(50), nullable=True)  # e.g. "9:40 AM"
    category = db.Column(db.String(50), default='activities')  # transport, stay, activities, meals
    cost = db.Column(db.Float, default=0.0)
    order_index = db.Column(db.Integer, default=1)
    day_number = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'section_id': self.section_id,
            'title': self.title,
            'description': self.description,
            'time_label': self.time_label,
            'category': self.category,
            'cost': self.cost,
            'order_index': self.order_index,
            'day_number': self.day_number
        }

    def __repr__(self):
        return f"<ItineraryItem {self.title}>"
