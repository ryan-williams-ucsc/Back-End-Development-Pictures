from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures"""
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"message": "No pictures found"}), 404

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return the URL of a picture by its ID"""
    # Find the picture with the specified id
    for picture in data:
        if picture.get("id") == id:
            return jsonify(picture), 200  # Return the picture data if found

    # If no picture is found, return a 404 error
    return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Get the JSON data from the request body
    picture = request.get_json()

    # Ensure the picture contains an "id" field
    if not picture or "id" not in picture:
        return jsonify({"Message": "Invalid picture data, 'id' is required"}), 400

    # Check if a picture with the provided ID already exists
    for pic in data:
        if pic.get("id") == picture["id"]:
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Append the picture to the data list
    data.append(picture)

    # Return a success response with the newly created picture data
    return jsonify(picture), 201
######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract picture data from the request body
    picture_data = request.get_json()

    # Find the picture by its ID in the data list
    picture = next((item for item in data if item.get("id") == id), None)

    # Check if the picture exists
    if picture is None:
        return jsonify({"message": "picture not found"}), 404

    # Update the picture with incoming request data
    picture.update(picture_data)

    # Respond with the updated picture and status code 200
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by ID."""
    # Find picture by id
    picture = next((item for item in data if item.get("id") == id), None)

    # Check if the picture exists
    if picture:
        # Remove picture from data list
        data.remove(picture)
        return "", 204  # HTTP 204 No Content

    # If picture does not exist, return 404
    return jsonify({"message": "picture not found"}), 404
