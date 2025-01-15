import os

from flask import Flask, jsonify, Response, request, send_file
from flask_cors import CORS 

import psycopg2
from psycopg2.extras import RealDictCursor

from datetime import datetime
from zoneinfo import ZoneInfo

import uuid

# from PIL import Image

import hash_trie

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

TEST_IMAGES_DIR = os.path.join(os.path.abspath('./'),"test_images")


DB_CONFIG={
    'host': 'localhost',
    'database': 'postgres',
    'user': 'photelo',
    'password': 'photelo'
}
#photelo is SCHEMA!!!

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


@app.route("/ping")
def ping_pong():
    return jsonify("PONG")

@app.route("/images/gallery")
def get_all_image_metadata():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
    select * FROM images;
        """)
    #TODO this query should have search parameters
    metadata = cursor.fetchall()
    cursor.close()
    conn.close()

    for item in metadata:
        item["id"] = uuid.UUID(item["id"]).hex
    if metadata:
        return jsonify(metadata)
    else:
        return jsonify({'error': 'Metadata not found'}), 404


# @app.route('/image_library/<uuid:image_id>', methods = ['GET'])
# def get_image_data(image_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         image_path = hash_trie.retrieve_file_path(image_id)
#         return(jsonify(""))
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    

@app.route('/images/<image_uuid>', methods = ['GET', 'PUT', 'DELETE'])
@app.route('/images', methods=['POST'])
def all_images(image_uuid = None):
    
    response_object = {'status': 'success'}
    if request.method == 'GET':
            
        try:
            image_path = hash_trie.retrieve_file_path(image_uuid)
            return send_file(image_path, mimetype='image/jpeg')
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    if request.method == 'POST':
        
        post_data = request.get_json()
        image_file = post_data["data"]
        image_name = post_data["name"]

        # hash_trie.insert_file(image_data)
        #### ADD DATA TO DATABASE

        filepath = os.path.join(TEST_IMAGES_DIR, image_name)
        image_file.save(filepath)

        response_object["message"] = "File uploaded successfully"
        response_object["path"] = filepath #TODO remove this
        return jsonify(response_object)


    # if 

if __name__ == "__main__":
    # flush db images
    # upload images
    app.run()


# @app.route("/image/create"):

# @app.route("/image/retrieve"):
# def retrieve_image():
#     #will only actually return image metadata

# @app.route("/image/update"):
# def update_image():
#     #for updating metadata
#     #should check for permissions

# @app.route("/image/delete"):
# def delete_image():
#     return null