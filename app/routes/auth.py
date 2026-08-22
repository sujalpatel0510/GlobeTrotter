from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db
from app.models.user import User
from app.utils.helpers import save_uploaded_image

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/index.html', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        identifier = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not identifier or not password:
            flash('Please enter both username/email and password.', 'error')
            return render_template('index.html')

        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated.', 'error')
                return render_template('index.html')
            
            login_user(user, remember=True)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials. Please check your username and password.', 'error')

    return render_template('index.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
@auth_bp.route('/register.html', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        first_name = request.form.get('first_name') or request.form.get('first-name', '').strip()
        last_name = request.form.get('last_name') or request.form.get('last-name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        phone = request.form.get('phone', '').strip()
        city = request.form.get('city', '').strip()
        country = request.form.get('country', '').strip()
        about = request.form.get('about', '').strip()

        if not first_name or not email:
            flash('First name and Email address are required.', 'error')
            return render_template('register.html')

        if not password:
            password = 'password123'

        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists. Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        username = email.split('@')[0]
        existing_u = User.query.filter_by(username=username).first()
        if existing_u:
            username = f"{username}_{User.query.count() + 1}"

        avatar_url = None
        if 'photo' in request.files:
            file = request.files['photo']
            avatar_url = save_uploaded_image(file, subfolder='avatars')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            city=city,
            country=country,
            about=about,
            avatar_url=avatar_url
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('main.dashboard'))

    return render_template('register.html')


@auth_bp.route('/guest-login')
def guest_login():
    """Logs in as demo user Maya Rao."""
    demo_user = User.query.filter_by(email='maya@example.com').first()
    if not demo_user:
        demo_user = User(
            first_name='Maya',
            last_name='Rao',
            username='maya.wanders',
            email='maya@example.com',
            city='Ahmedabad',
            country='India',
            about='Slow traveler, street food enthusiast.'
        )
        demo_user.set_password('password123')
        db.session.add(demo_user)
        db.session.commit()

    login_user(demo_user)
    return redirect(url_for('main.dashboard'))


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
