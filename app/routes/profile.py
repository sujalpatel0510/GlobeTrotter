from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from app.models import db
from app.models.trip import Trip
from app.utils.helpers import save_uploaded_image

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def view_profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        language = request.form.get('language', 'English').strip()
        city = request.form.get('city', '').strip()

        if not full_name or not email:
            flash('Full name and email are required.', 'error')
            return redirect(url_for('profile.view_profile'))

        # Split full name into first and last
        parts = full_name.split(' ', 1)
        current_user.first_name = parts[0]
        current_user.last_name = parts[1] if len(parts) > 1 else ''
        current_user.email = email
        current_user.language = language
        current_user.city = city

        if 'avatar' in request.files:
            file = request.files['avatar']
            avatar_url = save_uploaded_image(file, subfolder='avatars')
            if avatar_url:
                current_user.avatar_url = avatar_url

        db.session.commit()
        flash('Profile settings saved successfully!', 'success')
        return redirect(url_for('profile.view_profile'))

    # Load preplanned and previous trips
    user_trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).all()
    preplanned_trips = [t for t in user_trips if t.status in ('draft', 'upcoming', 'ongoing')][:3]
    previous_trips = [t for t in user_trips if t.status == 'completed'][:3]

    return render_template(
        'profile.html',
        user=current_user,
        preplanned_trips=preplanned_trips,
        previous_trips=previous_trips
    )


@profile_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted permanently.', 'info')
    return redirect(url_for('auth.login'))
