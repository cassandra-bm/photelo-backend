import psycopg2
import os

import random

import hash_trie
import uuid

# Database connection details
DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'photelo',
    'password': 'photelo'
}

# Function to connect to the database
def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        exit()

# Function to insert multiple images and metadata in bulk
def bulk_insert_images(conn, images_metadata):
    try:
        cursor = conn.cursor()

        insert_metadata_query = """
            INSERT INTO images (id, name, rating, tags)
            VALUES (%s, %s, %s, %s);
        """
        
        # Loop through the images and metadata
        for image_path, metadata in images_metadata:
            
            file_id = uuid.uuid4().hex
            cursor.execute(
                insert_metadata_query,
                (file_id, metadata['name'], metadata['rating'], metadata['tags'])
            )
            hash_trie.insert_file(image_path, file_id)

        # Commit the transaction
        conn.commit()
        print(f"Successfully inserted {len(images_metadata)} images and metadata records.")

    except Exception as e:
        print("Error during bulk insert:", e)
        conn.rollback()

# Function to gather image paths and assign metadata
def get_images_with_metadata(directory):
    sample_tags = ["spicy", "bulk", "test"]

    images_metadata = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('jpg', 'jpeg', 'png', 'gif')):
            image_path = os.path.join(directory, filename)
            
            # Example metadata (you can customize this logic)
            metadata = {
                'name': os.path.splitext(filename)[0],  # Use the filename (without extension) as name
                'rating': 1200.0,                        # Default rating
                'tags': random.sample(sample_tags, random.randint(0,len(sample_tags)))              # Default tags
            }
            images_metadata.append((image_path, metadata))
    return images_metadata

# Main function
def main():
    conn = connect_to_db()

    # Directory containing images
    image_directory = 'test_images'  # Replace with your directory path

    # Collect images and metadata
    images_metadata = get_images_with_metadata(image_directory)
    # print(len(images_metadata))
    if images_metadata:
        # Perform bulk insert
        bulk_insert_images(conn, images_metadata)
    else:
        print("No valid images found in the directory.")

    conn.close()

if __name__ == '__main__':
    main()


# CREATE TABLE image_metadata (
#     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- Unique identifier
#     name VARCHAR(100) NOT NULL,                     -- Name of the image
#     upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Timestamp of the upload
#     rating REAL,                                    -- Rating (float equivalent in PostgreSQL)
#     tags TEXT[],                                    -- Array of tags
#     metadata_id UUID NOT NULL,                     -- Foreign key linking to the images table
#     CONSTRAINT fk_images FOREIGN KEY (metadata_id) REFERENCES images(id) ON DELETE CASCADE
# );


