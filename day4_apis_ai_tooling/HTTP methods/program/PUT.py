from flask import Flask, jsonify, request

app = Flask(__name__)

books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):

    book = next((b for b in books_db if b["id"] == book_id), None)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()

    if "title" in data:
        book["title"] = data["title"]

    if "author" in data:
        book["author"] = data["author"]

    return jsonify(book), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)