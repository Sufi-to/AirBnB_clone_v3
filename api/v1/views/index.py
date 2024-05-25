#!/usr/bin/python3
"""Script that contains the routes to the database"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the api"""
    return jsonify(status='ok')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    """Returns the status of the api"""
    return jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        places=storage.count('Place'),
        reviews=storage.count('Review'),
        states=storage.count('State'),
        users=storage.count('User')
    )
