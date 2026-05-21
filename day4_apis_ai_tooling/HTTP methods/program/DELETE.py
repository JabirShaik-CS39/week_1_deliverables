from flask import Flask, jsonify

app = Flask(__name__)

books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):

    global books_db

    book = next((b for b in books_db if b["id"] == book_id), None)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    books_db = [b for b in books_db if b["id"] != book_id]

    return jsonify({"message": f"Book {book_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)