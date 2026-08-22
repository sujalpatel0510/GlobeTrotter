from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from app.models import db
from app.models.trip import Trip
from app.models.user import User
from app.utils.helpers import save_uploaded_image

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET', 'POST'])
@profile_bp.route('/profile.html', methods=['GET', 'POST'])
def view_profile():
    user = current_user if current_user.is_authenticated else User.query.first()
    
    if request.method == 'POST' and user:
        full_name = request.form.get('full_name') or request.form.get('p-name', '').strip()
        email = request.form.get('email') or request.form.get('p-email', '').strip().lower()
        language = request.form.get('language') or request.form.get('p-lang', 'English').strip()
        city = request.form.get('city') or request.form.get('p-city', '').strip()

        if full_name:
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
        if email:
            user.email = email
        user.language = language
        user.city = city

        if 'avatar' in request.files:
            file = request.files['avatar']
            avatar_url = save_uploaded_image(file, subfolder='avatars')
            if avatar_url:
                user.avatar_url = avatar_url

        db.session.commit()
        return redirect(url_for('profile.view_profile'))

    user_trips = Trip.query.filter_by(user_id=user.id).order_by(Trip.created_at.desc()).all() if user else []
    preplanned_trips = [t for t in user_trips if t.status in ('draft', 'upcoming', 'ongoing')][:3]
    previous_trips = [t for t in user_trips if t.status == 'completed'][:3]

    return render_template(
        'profile.html',
        user=user,
        preplanned_trips=preplanned_trips,
        previous_trips=previous_trips
    )


@profile_bp.route('/profile/delete-account', methods=['POST'])
def delete_account():
    user = current_user if current_user.is_authenticated else User.query.first()
    if user:
        if current_user.is_authenticated:
            logout_user()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('auth.login'))
