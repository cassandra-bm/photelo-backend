import os

from flask import Flask, jsonify, Response, request
from flask_cors import CORS 

import psycopg2
from psycopg2.extras import RealDictCursor

from datetime import datetime
from zoneinfo import ZoneInfo

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

#test images
# image_metadata = []
# for i in range(10):
#     image_data = {
#         "name": f"""test_image_{i}""",
#         "date": datetime.now(),
#         "rating": 1200,
#         "tags": [],
#         "uuid": i,
#         "url": f"""https://picsum.photos/id/{i}/200"""
#     }
#     # url = f"""https://picsum.photos/id/{i}/200"""
#     image_metadata.append(image_data)

@app.route("/ping")
def ping_pong():
    return jsonify("PONG")

@app.route("/images/gallery")
def get_all_image_metadata():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
    select * FROM image_metadata;
        """)
    metadata = cursor.fetchall()
    cursor.close()
    conn.close()

    if metadata:
        return jsonify(metadata)
    else:
        return jsonify({'error': 'Metadata not found'}), 404


@app.route('/image_library/<uuid:image_id>', methods = ['GET'])
def get_image_data(image_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        image_path = hash_trie.retrieve_file_path(image_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # try:
    #     # Query for the binary image data
    #     cursor.execute("SELECT image FROM images WHERE id = %s;", (str(image_id),))
    #     image = cursor.fetchone()

    #     if image is None:
    #         return jsonify({'error': 'Image not found'}), 404

    #     image_binary = image[0]  # Extract binary data

    #     cursor.close()
    #     conn.close()

    #     # Send the image as a binary response with the correct MIME type
    #     return Response(image_binary, content_type='image/jpeg')  # Change to the appropriate MIME type
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

@app.route('/images/<uuid:image_id>', methods = ['GET', 'PUT', 'DELETE'])
@app.route('/images', methods=['POST'])
def all_images(uuid = None):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        image_file = post_data["data"]
        image_name = post_data["name"]

        # hash_trie.insert_file(image_data)
        #### ADD DATA TO DATABASE

        filepath = os.path.join(TEST_IMAGES_DIR, image_name)
        image_file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "path": filepath})


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