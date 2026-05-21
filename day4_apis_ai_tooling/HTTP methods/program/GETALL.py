from flask import Flask, jsonify

app = Flask(__name__)

books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]

@app.route('/books', methods=['GET'])
def get_books():

    return jsonify({"books": books_db}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)