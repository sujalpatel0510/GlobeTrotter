from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.models import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=True, default='')
    username = db.Column(db.String(80), unique=True, index=True, nullable=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    city = db.Column(db.String(100), nullable=True, default='')
    country = db.Column(db.String(100), nullable=True, default='')
    about = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    language = db.Column(db.String(50), default='English')
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    trips = db.relationship('Trip', backref='owner', cascade='all, delete-orphan', lazy='dynamic')
    community_posts = db.relationship('CommunityPost', backref='author', cascade='all, delete-orphan', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return name if name else (self.username or self.email.split('@')[0])

    @property
    def initial(self):
        if self.first_name:
            return self.first_name[0].upper()
        if self.username:
            return self.username[0].upper()
        return 'T'

    @property
    def display_avatar(self):
        if self.avatar_url:
            if self.avatar_url.startswith('http') or self.avatar_url.startswith('/'):
                return self.avatar_url
            return f"/{self.avatar_url}"
        return "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"

    @property
    def trips_count(self):
        return self.trips.count()

    @property
    def wishlist_countries_count(self):
        # Default or calculated country wishlist count
        return 86

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'city': self.city,
            'country': self.country,
            'about': self.about,
            'avatar_url': self.avatar_url,
            'language': self.language,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'trips_count': self.trips_count,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else ''
        }

    def __repr__(self):
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
