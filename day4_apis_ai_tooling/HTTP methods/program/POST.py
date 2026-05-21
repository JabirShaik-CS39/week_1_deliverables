from flask import Flask, jsonify, request

POST = Flask(__name__)

books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]

@POST.route('/books', methods=['POST'])
def create_book():

    data = request.get_json()

    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Missing title or author"}), 400

    new_book = {
        "id": len(books_db) + 1,
        "title": data["title"],
        "author": data["author"]
    }

    books_db.append(new_book)

    print(books_db)

    return jsonify(new_book), 201

if __name__ == '__main__':
    POST.run(debug=True, port=5000)