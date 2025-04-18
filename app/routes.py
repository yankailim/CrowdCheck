from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Post, TruthVote
from .models import User
from flask import session, flash
from collections import Counter

bp = Blueprint('main', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Logged in as {username}', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Username not found. Try again.', 'warning')

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('main.index'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already taken. Choose another.', 'warning')
            return redirect(url_for('main.signup'))

        # Create new user
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()

        # Log them in right away
        session['user_id'] = new_user.id
        flash('Account created and logged in!', 'success')
        return redirect(url_for('main.index'))

    return render_template('signup.html')

@bp.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    user = None
    # Get user from session if they are logged in
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('index.html', posts=posts, user=user)


@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('submit.html')

@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)

    if 'user_id' not in session:
        flash('You must be logged in to vote', 'warning')
        return redirect(url_for('main.login'))

    current_user = User.query.get(session['user_id'])

    existing_vote = TruthVote.query.filter_by(post_id=post_id, user_id=current_user.id).first()

    if request.method == 'POST':
        vote = request.form['vote']
        if existing_vote:
            existing_vote.vote = vote
            flash('Your vote has been updated!', 'success')
        else:
            new_vote = TruthVote(vote=vote, post_id=post_id, user_id=current_user.id)
            db.session.add(new_vote)
            flash('Your vote has been recorded!', 'success')
        db.session.commit()

    votes = TruthVote.query.filter_by(post_id=post_id).all()
    user_vote = existing_vote.vote if existing_vote else None

    # Count votes
    vote_labels = ['True', 'Misleading', 'Fake', 'Unclear']
    vote_counts = Counter([v.vote for v in votes])
    chart_data = [vote_counts.get(label, 0) for label in vote_labels]

    # Determine majority vote
    majority_vote = vote_counts.most_common(1)[0][0] if vote_counts else "No votes yet"

    return render_template(
        'post.html',
        post=post,
        votes=votes,
        user_vote=user_vote,
        vote_labels=vote_labels,
        chart_data=chart_data,
        majority_vote=majority_vote
    )
