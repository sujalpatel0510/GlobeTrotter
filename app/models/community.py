from datetime import datetime
from app.models import db


class CommunityPost(db.Model):
    __tablename__ = 'community_posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=True)
    trip_name = db.Column(db.String(150), nullable=True)  # cached or custom trip title
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200), nullable=True)       # e.g., "Japan,Budget tip"
    avatar_color_class = db.Column(db.String(50), default='')  # e.g. 'teal', 'coral', 'gold'
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    @property
    def time_ago_str(self):
        if not self.created_at:
            return "Just now"
        delta = datetime.utcnow() - self.created_at
        seconds = delta.total_seconds()
        
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}m ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours}h ago"
        else:
            days = int(seconds / 86400)
            return f"{days}d ago"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'author_name': self.author.full_name if self.author else 'Traveler',
            'trip_id': self.trip_id,
            'trip_name': self.trip_name or (self.trip.name if self.trip else ''),
            'content': self.content,
            'tags': self.tags_list,
            'likes_count': self.likes_count,
            'time_ago': self.time_ago_str,
            'created_at': self.created_at.isoformat() if self.created_at else ''
        }

    def __repr__(self):
        return f"<CommunityPost {self.id} by User {self.user_id}>"
