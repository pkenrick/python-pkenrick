import pytest
from app import app, db
from app.models import User, Post
from config import Config


@pytest.fixture()
def init_database():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()

def test_set_password_saves_hashed_password():
    user = User(username='user1')
    user.set_password('test_password')
    assert not user.check_password('wrong_password')
    assert user.check_password('test_password')

def test_avatar():
    user = User(username='user1', email='user1@email.com')
    assert user.avatar() == 'https://www.gravatar.com/avatar/3acc837f898bdaa338b7cd7a9ab6dd5b?d=identicon&s=80'


def test_follow(init_database):
    user1 = User(username='user1')
    user2 = User(username='user2')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    assert user1.followed.all() == []
    assert user2.followed.all() == []

    user2.follow(user1)
    db.session.commit()

    assert user2.is_following(user1)
    assert user2.followed.all() == [user1]
    assert user1.followers.all() == [user2]

    user2.unfollow(user1)
    db.session.commit()

    assert not user2.is_following(user1)
    assert user2.followed.all() == []
    assert user1.followers.all() == []

def test_follow_posts(init_database):
    user1 = User(username='user1')
    user2 = User(username='user2')
    user3 = User(username='user3')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    assert user2.followed_posts().all() == []

    post1 = Post(body='This is a post 1', author=user1)
    post2 = Post(body='This is a post 2', author=user2)
    post3 = Post(body='This is a post 3', author=user3)
    user3.follow(user1)
    db.session.commit()

    followed_posts = user3.followed_posts().all()
    assert len(followed_posts) == 2
    assert post1 in followed_posts
    assert post3 in followed_posts
