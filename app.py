import os

from flask import Flask, jsonify, Response, request, send_file
from flask_cors import CORS 

import psycopg2
from psycopg2.extras import RealDictCursor

from datetime import datetime
from zoneinfo import ZoneInfo

import uuid

from werkzeug.utils import secure_filename


# from PIL import Image

import hash_trie
from elo import get_new_ratings

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

TEST_IMAGES_DIR = os.path.join(os.path.abspath('./'),"test_images")
LOCAL_DIRECTORY = os.path.abspath('./')

DB_CONFIG={
    'host': 'localhost',
    'database': 'postgres',
    'user': 'photelo',
    'password': 'photelo'
}
#photelo is SCHEMA!!!
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        exit()


def insert_file(file, name, tags = []):
    #generate uuid 
    file_id = uuid.uuid4().hex
    file_name = name
    file_rating = 1200
    file_tags = tags

    #attempt insertion
    #attempt to save file in hash trie location 
    
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()

        insert_metadata_query = """
            INSERT INTO images (id, name, rating, tags)
            VALUES (%s, %s, %s, %s);
        """
        
        # Loop through the images and metadata
        # for image_path, metadata in images_metadata:
            
        file_id = uuid.uuid4().hex
        cursor.execute(
            insert_metadata_query,
            (file_id, file_name, file_rating, file_tags)
        )
        file_dir = hash_trie.get_path_from_uuid(file_id)
        file_path = os.path.join(file_dir, file.name)
        os.makedirs(file_dir)
        file.save(file_path)

        # hash_trie.insert_file(image_path, file_id)

        # Commit the transaction
        conn.commit()
        
        # print(f"Successfully inserted {len(images_metadata)} images and metadata records.")

    except Exception as e:
        print("Error during insert:", e)
        conn.rollback()

    # return success

    #get path from hash trie

def update_elo_rating(winner_id, loser_id):
    try:

        app.logger.warning("Functional block start")
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT rating FROM images
            WHERE id = %s
        """, (winner_id,))  # Pass parameters as a tuple
        
        
        winner_rating = cursor.fetchone()["rating"]

        # winner_rating = cursor.fetchone()["rating"]

        cursor.execute("""
            SELECT rating FROM images
            WHERE id = %s
        """, (loser_id,))  # Pass parameters as a tuple
        
        loser_rating = cursor.fetchone()["rating"]
        # loser_rating = cursor.fetchone()["rating"]

        app.logger.warning("got past rating query")
        new_rating_winner, new_rating_loser = get_new_ratings(winner_rating, loser_rating)
        
        app.logger.warning("elo calc finished")

        update_query = """
            UPDATE images
            set rating = %s
            where id = %s
            """
        cursor.execute(
            update_query, (new_rating_winner, winner_id)
        )
        
        cursor.execute(
            update_query, (new_rating_loser, loser_id)
        )

        conn.commit()
        
        app.logger.warning("updates finished")

        app.logger.warning("new ratings")
        app.logger.warning(new_rating_winner)
        app.logger.warning(new_rating_loser)
    except Exception as e:
        app.logger.warning(e)
        return
    finally:
        cursor.close()
        conn.close()
    
# def get_elo_rating(winner_old, loser_old):


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
        return jsonify({'error': 'Metadata not found'}, 404)



@app.route('/images/<image_uuid>', methods = ['GET', 'PUT', 'DELETE'])
@app.route('/images/', methods=['POST'])
def all_images(image_uuid = None):
    
    response_object = {'status': 'success'}
    if request.method == 'GET':
            
        try:
            image_path = hash_trie.retrieve_file_path(image_uuid)
            return send_file(image_path, mimetype='image/jpeg')
        
        except Exception as e:
            return jsonify({'error': str(e)}, 500)

    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"error": "No file part"}, 400)

        file = request.files['image']

        if not file.filename:
            return jsonify({"error": "No selected file"}, 400)

        file_id = uuid.uuid4()
        # file_name = request.files['name']
        file_name = file.filename
        file_tags = [] #TODO implement
        try:
            insert_file(file,file_name,file_tags)
        except:
            return jsonify({"message": "an error'd"})

        # #todo hash trie upload
        # temp_file_path = os.path.join()
        # os.path.join()
        # file.save(f".//{filename}")  # Example save location

        return jsonify({"message": "File uploaded successfully", "filename": file_name}, 200)


@app.route('/vote/<winner_id>/<loser_id>', methods=["POST"])
@app.route('/vote/', methods=['GET'])
def vote(winner_id = "", loser_id = ""):
    response_object = {'status': 'success'}
    app.logger.info("vote request")
    if request.method == 'GET':

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute(
                """select * from images order by random() limit 2;"""
            )
            #TODO this query should have search parameters
            metadata = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(metadata)
        except:
            return jsonify({"message": "File uploaded successfully"})
        #TODO: make sure no duplicates???
        
    if request.method == 'POST':
        try:
        
            update_elo_rating(winner_id, loser_id)
            return jsonify({"message:": "we hit the voting block"})
        except:
            return jsonify({"message": "error'd"})

    return 
            

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