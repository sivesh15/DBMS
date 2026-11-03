
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

CREATE TABLE IF NOT EXISTS books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    category VARCHAR(80),
    quantity INT NOT NULL DEFAULT 0,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

INSERT INTO books (title, author, category, quantity, price)
VALUES
('Wings of Fire', 'A. P. J. Abdul Kalam', 'Biography', 5, 250.00),
('The Alchemist', 'Paulo Coelho', 'Fiction', 3, 300.00);

SELECT * FROM books;
