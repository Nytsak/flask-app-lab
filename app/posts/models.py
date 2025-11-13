from datetime import datetime
from app import db
import enum


class CategoryEnum(enum.Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    category = db.Column(
        db.Enum(CategoryEnum),
        default=CategoryEnum.other,
        nullable=False
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    author = db.Column(db.String(20), default='Anonymous', nullable=False)

    def __repr__(self):
        return f'<Post {self.id}: {self.title} by {self.author}>'
