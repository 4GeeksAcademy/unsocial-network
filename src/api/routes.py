"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import request, jsonify, Blueprint
from api.models import db, User, Post, Comment
from api.utils import APIException
from flask_cors import CORS

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route("/login", methods=["POST"])
def login():

    body = request.get_json()

    email = body.get("email", None)
    password = body.get("password", None)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    searched_user = User.query.filter_by(email=email).first()
    if not searched_user:
        return jsonify({"msg": "Bad email or password"}), 401

    if searched_user.password != password: # Compare passwords directly for simplicity but we will need hashes later
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200


@api.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()  # consulta la lista de usuarios en la DB

    list_of_json_users = [user.serialize() for user in users]

    return jsonify(list_of_json_users), 200


@api.route('/whoami', methods=['GET'])
@jwt_required()
def who_am_i():
    current_user = get_jwt_identity()

    user = User.get_by_email(current_user)
    if user is None:
        raise APIException('User not found', status_code=404)

    return jsonify(user.serialize()), 200


def reqVal(body, keys):
    vals = []
    for key in keys:
        if key not in body:
            raise APIException(
                f'You need to specify the {key}', status_code=400)
        vals.append(body[key])
    return vals


@api.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    keys = ['email', 'password', 'is_active']
    email, password, is_active = reqVal(body, keys)

    try:
        new_user = User(email=email, password=password,
                        is_active=bool(is_active))
        new_user.save()

    except Exception as e:
        raise APIException('Error creating the user: ' +
                           str(e), status_code=500)

    return jsonify(new_user.serialize()), 201


@api.route('/user/<string:email>')
def get_user_by_email(email):

    wanted = User.get_by_email(email)

    if wanted is None:
        raise APIException('User not found', status_code=404)

    return jsonify(wanted.serialize()), 200


@api.route('/user/<string:email>', methods=['PUT', 'DELETE'])
def update_user_by(email):

    edited = User.get_by_email(email)
    if edited is None:
        raise APIException('User not found', status_code=404)

    if request.method == 'DELETE':
        try:
            db.session.delete(edited)
            db.session.commit()

        except Exception as e:
            raise APIException('Error deleting the user: ' +
                               str(e), status_code=500)

        return jsonify({"msg": "User deleted"}), 200

    body = request.get_json()
    if 'is_active' not in body:
        raise APIException(
            'You need to specify the is_active field', status_code=400)

    if 'is_active' in body:
        try:
            edited.is_active = bool(body['is_active'])
            db.session.commit()
        except Exception as e:
            raise APIException('Error updating the user: ' +
                               str(e), status_code=500)

    return jsonify(edited.serialize()), 200


@api.route('/post/<int:user_id>', methods=['POST'])
def create_post(user_id):
    body = request.get_json()

    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    if 'content' not in body:
        raise APIException(
            'You need to specify the content field', status_code=400)

    content = body['content']

    post = Post()
    post.content = content
    post.user_id = user_id

    db.session.add(post)
    db.session.commit()

    return jsonify(post.serialize()), 201


@api.route('/post', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    list_of_json_posts = [post.serialize() for post in posts]

    return jsonify(list_of_json_posts), 200


@api.route('/comment/<int:post_id>', methods=['POST'])
def create_comment(post_id):
    body = request.get_json()
    keys = ['comment_text', 'author_id']
    comment_text, author_id = reqVal(body, keys)

    post = Post.query.get(post_id)
    if post is None:
        raise APIException('Post not found', status_code=404)

    author = User.query.get(author_id)
    if author is None:
        raise APIException('Author not found', status_code=404)

    comment = Comment()
    comment.comment_text = comment_text
    comment.post_id = post_id
    comment.author_id = author_id
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.serialize()), 201
