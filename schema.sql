
-- Create the images table
CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- Unique identifier
    image BYTEA NOT NULL                            -- Binary data for storing the image
);

-- Create the image_metadata table
CREATE TABLE image_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- Unique identifier
    name VARCHAR(100) NOT NULL,                     -- Name of the image
    upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Timestamp of the upload
    rating REAL,                                    -- Rating (float equivalent in PostgreSQL)
    tags TEXT[],                                    -- Array of tags
    image_id UUID NOT NULL,                     -- Foreign key linking to the images table
    CONSTRAINT fk_images FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
);