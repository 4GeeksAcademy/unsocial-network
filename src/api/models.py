from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def __init__(self, email, password, is_active=True):
        self.email = email
        self.password = password
        self.is_active = is_active

    def serialize(self):
        return {
            # "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
class Post(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(backref="posts")

    # comments - estan siendo creados automaticamente por el backref en Comment

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": self.user.serialize(),
            "comments": [comment.serialize() for comment in self.comments],
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str]= mapped_column(String(120))
    
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post : Mapped["Post"] = relationship(backref="comments")

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(backref="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "author":self.author.serialize()
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)

    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to: Mapped["User"] = relationship(
        foreign_keys=[user_to_id], backref="followers")

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_from: Mapped["User"] = relationship(
        foreign_keys=[user_from_id], backref="followings")

    def serialize(self):
        return {
            "id": self.id,
            "user_to_id": self.user_to_id,
            "user_to": self.user_to.serialize(),
            "user_from_id":self.user_from_id,
            "user_from": self.user_from.serialize()
        }
