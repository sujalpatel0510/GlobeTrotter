from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db
from app.models.community import CommunityPost
from app.models.trip import Trip

community_bp = Blueprint('community', __name__, url_prefix='/community')


@community_bp.route('/')
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
    user_trips = []
    if current_user.is_authenticated:
        user_trips = Trip.query.filter_by(user_id=current_user.id).all()

    return render_template('community.html', posts=posts, user_trips=user_trips, query=query)


@community_bp.route('/post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content', '').strip()
    tags = request.form.get('tags', '').strip()
    trip_id = request.form.get('trip_id', type=int)

    if not content:
        flash('Please enter some text for your post.', 'error')
        return redirect(url_for('community.feed'))

    trip_name = None
    if trip_id:
        trip = Trip.query.get(trip_id)
        if trip:
            trip_name = trip.name

    # Avatar color style
    colors = ['teal', 'coral', 'gold']
    color_class = colors[current_user.id % len(colors)]

    new_post = CommunityPost(
        user_id=current_user.id,
        trip_id=trip_id if trip_id else None,
        trip_name=trip_name,
        content=content,
        tags=tags,
        avatar_color_class=color_class
    )
    db.session.add(new_post)
    db.session.commit()

    flash('Your travel story has been shared with the community!', 'success')
    return redirect(url_for('community.feed'))


@community_bp.route('/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    post.likes_count = (post.likes_count or 0) + 1
    db.session.commit()
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'likes_count': post.likes_count})
        
    return redirect(url_for('community.feed'))
