-- DROP TABLE images; 

CREATE TABLE images (
    id CHAR(32) PRIMARY KEY,  -- Unique identifier
    name VARCHAR(100) NOT NULL,                     -- Name of the image
    upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Timestamp of the upload
    rating REAL,                                    -- Rating (float equivalent in PostgreSQL)
    tags TEXT[]                                     -- Array of tags
    -- image_id UUID NOT NULL,                     -- Foreign key linking to the images table
    -- CONSTRAINT fk_images FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
);