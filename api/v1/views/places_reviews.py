#!/usr/bin/python3
"""Script that handles all the views to handle all default restful api"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """Retrieves all the reviews of a place with the given id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def one_review(review_id):
    """Returns a review object with a give id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def rem_review(review_id):
    """Deletes a review object with a given id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def add_review(place_id):
    """Posts a new review to a the place with given id and return it"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    req_rev = request.get_json()
    if not req_rev:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_rev:
        abort(400, 'Missing user_id')
    id = req_rev['user_id']
    user = storage.get(User, id)
    if not user:
        abort(404)
    if 'text' not in req_rev:
        abort(400, 'Missing text')
    new_review = Review(**req_rev)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates the review object with the given id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    up_rev = request.get_json()
    if not up_rev:
        abort(400, 'Not a JSON')
    for key, value in up_rev.item():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'update_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
