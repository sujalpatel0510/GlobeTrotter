import secrets
from datetime import datetime, date
from app.models import db


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    start_place = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(255), nullable=True)
    pattern = db.Column(db.String(20), default='')  # e.g. 'pat-1', 'pat-2' for card styles
    total_budget = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='draft')  # draft, upcoming, ongoing, completed
    is_public = db.Column(db.Boolean, default=False)
    share_token = db.Column(db.String(64), unique=True, index=True, default=lambda: secrets.token_urlsafe(16))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sections = db.relationship('ItinerarySection', backref='trip', cascade='all, delete-orphan',
                               order_by='ItinerarySection.section_order', lazy='dynamic')
    community_posts = db.relationship('CommunityPost', backref='trip', lazy='dynamic')

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days + 1
            return max(1, days)
        return 1

    @property
    def total_spent(self):
        total = 0.0
        for section in self.sections:
            for item in section.items:
                total += (item.cost or 0.0)
        return round(total, 2)

    @property
    def budget_percentage(self):
        if not self.total_budget or self.total_budget <= 0:
            return 0
        return min(150, int((self.total_spent / self.total_budget) * 100))

    @property
    def is_over_budget(self):
        if self.total_budget and self.total_budget > 0:
            return self.total_spent > self.total_budget
        return False

    @property
    def daily_average(self):
        days = self.duration_days
        return round(self.total_spent / max(1, days), 2)

    @property
    def cities_count(self):
        sec_count = self.sections.count()
        return max(1, sec_count)

    @property
    def date_range_display(self):
        if not self.start_date or not self.end_date:
            return "TBD"
        
        start_month = self.start_date.strftime('%b').upper()
        end_month = self.end_date.strftime('%b').upper()
        
        if start_month == end_month:
            return f"{start_month} {self.start_date.day:02d}–{self.end_date.day:02d}"
        else:
            return f"{start_month} {self.start_date.day:02d} – {end_month} {self.end_date.day:02d}"

    @property
    def date_range_full(self):
        if not self.start_date or not self.end_date:
            return "Dates pending"
        return f"{self.start_date.strftime('%b %d')} – {self.end_date.strftime('%b %d')}"

    @property
    def budget_breakdown(self):
        """Calculates breakdown by category."""
        breakdown = {
            'transport': {'spent': 0.0, 'percentage': 0},
            'stay': {'spent': 0.0, 'percentage': 0},
            'activities': {'spent': 0.0, 'percentage': 0},
            'meals': {'spent': 0.0, 'percentage': 0}
        }
        
        for section in self.sections:
            for item in section.items:
                cat = (item.category or 'activities').lower()
                if cat in breakdown:
                    breakdown[cat]['spent'] += (item.cost or 0.0)
                else:
                    breakdown['activities']['spent'] += (item.cost or 0.0)
                    
        total = self.total_spent or 1.0
        for cat in breakdown:
            spent = breakdown[cat]['spent']
            breakdown[cat]['percentage'] = min(100, int((spent / total) * 100)) if total > 0 else 0
            breakdown[cat]['spent'] = round(spent, 2)
            
        return breakdown

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'start_place': self.start_place,
            'description': self.description,
            'total_budget': self.total_budget,
            'total_spent': self.total_spent,
            'status': self.status,
            'is_public': self.is_public,
            'share_token': self.share_token,
            'duration_days': self.duration_days,
            'cities_count': self.cities_count,
            'date_range_display': self.date_range_display,
            'sections': [s.to_dict() for s in self.sections]
        }

    def __repr__(self):
        return f"<Trip {self.name}>"
