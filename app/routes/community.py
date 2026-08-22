from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db
from app.models.community import CommunityPost
from app.models.trip import Trip
from app.models.user import User

community_bp = Blueprint('community', __name__)


@community_bp.route('/community')
@community_bp.route('/community.html')
def feed():
    query = request.args.get('q', '').strip()
    
    post_query = CommunityPost.query.order_by(CommunityPost.created_at.desc())
    if query:
        post_query = post_query.filter(
            CommunityPost.content.ilike(f'%{query}%') |
            CommunityPost.tags.ilike(f'%{query}%') |
            CommunityPost.trip_name.ilike(f'%{query}%')
        )
        
    posts = post_query.all()
    user_id = current_user.id if current_user.is_authenticated else 1
    user_trips = Trip.query.filter_by(user_id=user_id).all()

    return render_template('community.html', posts=posts, user_trips=user_trips, query=query)


@community_bp.route('/community/post', methods=['POST'])
def create_post():
    content = request.form.get('content', '').strip()
    tags = request.form.get('tags', '').strip()
    trip_id = request.form.get('trip_id', type=int)

    if not content:
        return redirect(url_for('community.feed'))

    trip_name = None
    if trip_id:
        trip = db.session.get(Trip, trip_id)
        if trip:
            trip_name = trip.name

    user_id = current_user.id if current_user.is_authenticated else 1
    colors = ['teal', 'coral', 'gold']
    color_class = colors[user_id % len(colors)]

    new_post = CommunityPost(
        user_id=user_id,
        trip_id=trip_id if trip_id else None,
        trip_name=trip_name,
        content=content,
        tags=tags,
        avatar_color_class=color_class
    )
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('community.feed'))


@community_bp.route('/community/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    post = db.session.get(CommunityPost, post_id)
    if not post:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Post not found'}), 404
        return redirect(url_for('community.feed'))

    post.likes_count = (post.likes_count or 0) + 1
    db.session.commit()
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'likes_count': post.likes_count})
        
    return redirect(url_for('community.feed'))
