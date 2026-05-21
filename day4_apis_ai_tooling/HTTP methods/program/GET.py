from flask import Flask, jsonify

app = Flask(__name__)

books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):

    book = next((b for b in books_db if b["id"] == book_id), None)

    if book:
        return jsonify(book), 200

    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)