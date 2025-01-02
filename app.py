from flask import Flask, jsonify, Response
from flask_cors import CORS 

import psycopg2
from psycopg2.extras import RealDictCursor

from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


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

@app.route("/image/gallery")
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
        # Query for the binary image data
        cursor.execute("SELECT image FROM images WHERE id = %s;", (str(image_id),))
        image = cursor.fetchone()

        if image is None:
            return jsonify({'error': 'Image not found'}), 404

        image_binary = image[0]  # Extract binary data

        cursor.close()
        conn.close()

        # Send the image as a binary response with the correct MIME type
        return Response(image_binary, content_type='image/jpeg')  # Change to the appropriate MIME type
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
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