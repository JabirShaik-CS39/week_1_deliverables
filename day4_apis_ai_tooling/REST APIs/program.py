from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data acting as our database
books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen"},
    {"id": 5, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}

]

class_db =[
    {"id": 1, "name": "Math 101", "teacher": "Mr. Smith"},
    {"id": 2, "name": "History 201", "teacher": "Ms. Johnson"},
    {"id": 3, "name": "Science 301", "teacher": "Dr. Brown"},
    {"id": 4, "name": "Literature 401", "teacher": "Mrs. Davis"},
    {"id": 5, "name": "Art 501", "teacher": "Ms. Wilson"}
]

# Home Route - So the bare link doesn't 404
@app.route('/class', methods=['GET'])
def get_class():
    return jsonify({"classes": class_db}), 200


# 1. GET Request - Fetch all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"books": books_db}), 200

# 2. GET Request - Fetch a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books_db if b["id"] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

# 3. POST Request - Add a new book
@app.route('/books', methods=['POST'])
def create_book():
    # Get JSON data sent by the user
    data = request.get_json()
    
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Missing title or author"}), 400
        
    new_book = {
        "id": len(books_db) + 1,
        "title": data["title"],
        "author": data["author"]
    }
    books_db.append(new_book)
    return jsonify(new_book), 201

# 4. DELETE Request - Remove a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books_db
    book = next((b for b in books_db if b["id"] == book_id), None)
    if book:
        books_db = [b for b in books_db if b["id"] != book_id]
        return jsonify({"result": f"Book {book_id} deleted"}), 200
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    # Starts the local development server
    app.run(debug=True, port=5000)