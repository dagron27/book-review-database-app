from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to your SQLite database file (relative to the process's
# working directory, which is the repository root -- see README/CI, which
# invoke this as `python src/app.py` from the repo root).
DATABASE = 'data/books.db'

# << ADDED CODE #1 >>
# Method created because connection used in more than one other method
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books")
        books = cursor.fetchall()
        conn.close()

        # Convert the list of tuples into a list of dictionaries
        book_list = []
        for book in books:
            book_dict = {
                'book_id': book[0],
                'title': book[1],
                'publication_year': book[2]
                # Add other attributes here as needed
            }
            book_list.append(book_dict)

        return jsonify({'books': book_list})
    except Exception as e:
        app.logger.error("Error in get_all_books: %s", e)
        return jsonify({'error': 'An error occurred processing your request.'}), 500

# API to get all authors
@app.route('/api/authors', methods=['GET'])
def get_all_authors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Authors")
        authors = cursor.fetchall()
        conn.close()
        return jsonify(authors)
    except Exception as e:
        app.logger.error("Error in get_all_authors: %s", e)
        return jsonify({'error': 'An error occurred processing your request.'}), 500

# API to get all reviews
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reviews")
        reviews = cursor.fetchall()
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        app.logger.error("Error in get_all_reviews: %s", e)
        return jsonify({'error': 'An error occurred processing your request.'}), 500

# API to add a book to the database
@app.route('/api/add_book', methods=['POST'])
def add_book():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get book details from the request
        data = request.get_json()
        title = data.get('title')
        publication_year = data.get('publication_year')

        # Insert the book into the database
        cursor.execute("INSERT INTO Books (title, publication_year) VALUES (?, ?)", (title, publication_year))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Book added successfully'})
    except Exception as e:
        app.logger.error("Error in add_book: %s", e)
        return jsonify({'error': 'An error occurred processing your request.'}), 500

# << ADDED CODE # 1>>
# API to search for books by year
@app.route('/api/books/<int:year>', methods=['GET'])
def get_books_by_year(year):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books WHERE publication_year = ?", (year,))
        books = cursor.fetchall()
        conn.close()

        # Convert the list of tuples into a list of dictionaries
        book_list = []
        for book in books:
            book_dict = {
                'book_id': book[0],
                'title': book[1],
                'publication_year': book[2]
                # Add other attributes here as needed
            }
            book_list.append(book_dict)

        return jsonify({'books': book_list})
    except Exception as e:
        app.logger.error("Error in get_books_by_year: %s", e)
        return jsonify({'error': 'An error occurred processing your request.'}), 500

# API to view the current user's account (username, email, reviews).
# Hardcoded to user_account_id = 1: this app has no login/session system,
# matching the original assignment's single-user demo scope (see README.md
# "Assignment Intent"). This endpoint was briefly removed during an earlier
# security-hardening pass, then restored after confirming it was the
# assignment's actual graded requirement rather than an accidental exposure
# to fix -- see README.md "Known Issues" for the full history.
@app.route('/api/user_account', methods=['GET'])
def get_user_account():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Users.user_id, Users.username, Users.email
            FROM user_account
            JOIN Users ON user_account.user_id = Users.user_id
            WHERE user_account.user_account_id = 1
        """)
        user = cursor.fetchone()

        if user is None:
            conn.close()
            return jsonify({'error': 'User account not found'}), 404

        cursor.execute(
            "SELECT rating, review_text, review_date FROM Reviews WHERE user_id = ?",
            (user['user_id'],)
        )
        reviews = cursor.fetchall()
        conn.close()

        review_list = [
            {
                'rating': review['rating'],
                'review_text': review['review_text'],
                'review_date': review['review_date']
            }
            for review in reviews
        ]

        return jsonify({
            'username': user['username'],
            'email': user['email'],
            'reviews': review_list
        })
    except Exception as e:
        app.logger.error("Error in get_user_account: %s", e)
        return jsonify({'error': 'An error occurred processing your request.'}), 500

@app.route('/api/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title, publication_year FROM Books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        conn.close()

        if book is None:
            return jsonify({'error': 'Book not found'}), 404

        return jsonify({'title': book['title'], 'publication_year': book['publication_year']})
    except Exception as e:
        app.logger.error("Error in get_book: %s", e)
        return jsonify({'error': 'An error occurred processing your request.'}), 500

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
