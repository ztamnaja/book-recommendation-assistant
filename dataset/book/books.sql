-- Create the books table
CREATE TABLE IF NOT EXISTS books (
    isbn13 VARCHAR(13) NOT NULL PRIMARY KEY,
    isbn10 VARCHAR(10),
    title VARCHAR(510),
    subtitle VARCHAR(510),
    authors TEXT,
    categories TEXT,
    thumbnail TEXT DEFAULT NULL,
    description TEXT DEFAULT NULL,
    published_year INT DEFAULT NULL,
    average_rating FLOAT DEFAULT NULL,
    num_pages INT DEFAULT NULL,
    ratings_count INT DEFAULT NULL
);

-- Load data from CSV into the books table
LOAD DATA INFILE '/var/lib/mysql-files/books.csv'
INTO TABLE books
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(isbn13, isbn10, title, subtitle, authors, categories, thumbnail, description, published_year, @average_rating, num_pages, ratings_count)
SET
    average_rating = NULLIF(@average_rating, '');