from app.models import db


class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)  # e.g., "Kyoto", "Lisbon"
    country = db.Column(db.String(100), nullable=False)                         # e.g., "Japan", "Portugal"
    cost_index = db.Column(db.String(20), default='medium')                     # low ($), medium ($$), high ($$$)
    image_pattern = db.Column(db.String(20), default='')                       # '', 'pat-1', 'pat-2'
    description = db.Column(db.Text, nullable=True)
    trips_count = db.Column(db.Integer, default=0)
    trend = db.Column(db.String(20), default='↑ 5%')

    # Relationships
    activities = db.relationship('Activity', backref='destination', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def cost_symbol(self):
        mapping = {'low': '$', 'medium': '$$', 'high': '$$$'}
        return mapping.get(self.cost_index.lower(), '$$')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'cost_index': self.cost_index,
            'cost_symbol': self.cost_symbol,
            'image_pattern': self.image_pattern,
            'description': self.description,
            'trips_count': self.trips_count,
            'trend': self.trend,
            'activities_count': self.activities.count()
        }

    def __repr__(self):
        return f"<Destination {self.name}, {self.country}>"


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False, index=True)               # e.g. "Tandem paragliding over Pokhara"
    category = db.Column(db.String(50), default='Adventure', index=True)       # Adventure, Food & Drink, Culture, Experience, etc.
    price = db.Column(db.Float, default=0.0)
    duration = db.Column(db.String(50), nullable=True)                         # e.g. "45 min flight", "3 hr walking tour"
    description = db.Column(db.Text, nullable=True)                            # e.g. "includes pickup · from $85"
    stamp_color = db.Column(db.String(20), default='coral')                    # coral, teal, gold
    bookings_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'destination_id': self.destination_id,
            'destination_name': self.destination.name if self.destination else '',
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'duration': self.duration,
            'description': self.description,
            'stamp_color': self.stamp_color,
            'bookings_count': self.bookings_count
        }

    def __repr__(self):
        return f"<Activity {self.name}>"
