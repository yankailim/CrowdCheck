from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

class TruthVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.String(20))  # True, Misleading, Fake, Unclear
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_vote'),
    )

class Highlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_index = db.Column(db.Integer)
    end_index = db.Column(db.Integer)
    comment = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
