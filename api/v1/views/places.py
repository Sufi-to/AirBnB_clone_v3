#!/usr/bin/python3
"""Script for configuring the places api"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """Returns all the places related to the given city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def one_place(place_id):
    """Retrieves a place object with a given id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def rem_place(place_id):
    """Deletes a place object with a given id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Posts a new place using an http post request"""
    city_id = storage.get(City, city_id)
    if not city_id:
        abort(404)
    req_place = request.get_json()
    if not req_place:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_place:
        abort(400, 'Missing user_id')
    u_id = req_place['user_id']
    user_id = storage.get(User, u_id)
    if not user_id:
        abort(404)
    if 'name' not in req_place:
        abort(400, 'Missing name')
    new_place = Place(**req_place)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Return a place object with the updated data"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    req_place = request.get_json()
    if not req_place:
        abort(400, 'Not a JSON')
    for key, value in req_place.items():
        if key not in ['id', 'city_id', 'user_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
