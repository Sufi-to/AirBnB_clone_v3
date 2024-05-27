#!/usr/bin/python3
"""Script for the user views api"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves all the users from the database"""
    user_objs = storage.all(User)
    return jsonify([user.to_dict() for user in user_objs.values()])


@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def one_user(user_id):
    """Retrieves a user object with the specified id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def rem_user(user_id):
    """Deletes a user with a specified user id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Creates a user"""
    user_new = request.get_json()
    if not user_new:
        abort(400, "Not a JSON")
    if 'email' not in user_new:
        abort(400, "Missing email")
    if 'password' not in user_new:
        abort(400, "Missing password")
    user = User(**user_new)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Returns the updated user object with status code 200"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a JSON")
    for key, value in put_req.items():
        if key not in ('id', 'email', 'created_at', 'updated_id'):
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
