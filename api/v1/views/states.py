# #!/usr/bin/python3
# """Script that contains routes to the states table"""
# from flask import abort, jsonify, make_response
# from api.v1.views import app_views
# from models import storage
# from models.state import State


# @app_views.route('/states', methods=['GET'], strict_slashes=False)
# def states():
#     """Returns all the states in the database"""
#     states = storage.all(State)
#     return jsonify([state.to_dict() for state in states.values()])


# @app_views.route('/states/<states_id>', methods=['GET'], strict_slashes=False)
# def state(state_id):
#     """Returns the state with the particular id"""
#     state = storage.get(State, state_id)
#     if not state:
#         abort(404)
#     return jsonify(state.to_dict())


# @app_views.route('/states/<states_id>', methods=['DELETE'], strict_slashes=False)
# def state(state_id):
#     """Returns the state with the particular id"""
#     state = storage.get(State, state_id)
#     if not state:
#         abort(404)
#     state.delete()
#     storage.save()
#     return make_response(jsonify({}), 200)
