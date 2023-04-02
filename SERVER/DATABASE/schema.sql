DROP TABLE IF EXISTS images;

CREATE TABLE images (
    /*Unique identifier for each image*/
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    /*Time when image was added to the database*/
    time_logged TIMESTAMP NOT NULL,
    /*ID of drone from which this image originated*/
    drone_id INTEGER NOT NULL,
    /*Time when iage was captured*/
    time_captured TIMESTAMP NOT NULL,
    /*Coordinates where the  image was taken*/
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    /*Prediciton from ML model*/
    prediction STRING check(prediction in ('FIRE', 'NO_FIRE')),
    /*Label (correct answer) for image, if user provides*/
    label STRING DEFAULT NULL check(label in (NULL, 'FIRE', 'NO_FIRE')),
    /*Blob of the image data. Use to reconstruct image*/
    image BLOB NOT NULL
);