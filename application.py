from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(120))
    

    def __repr__(self):
        return f"{self.book_name} - {self.publisher} - {self.author}"



@app.route('/')
def index():
    return 'Hello!'


@app.route('/books')
def get_books():
    books = Book.query.all()

#    with app.app_context():
#        db.create_all()
#        import Book
#        book = (Book(book_name="Grape Soda", publisher="Tastes like grapes")),
#        db.session.add(Book(book_name="Cherry", publisher="Tastes like that one ice cream"))

    output = []
    for book in books:
        book_data = {'book_name': book.book_name, 'publisher': book.publisher, 'author': book.author}

        output.append(book_data)
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"book_name": book.book_name, "publisher": book.publisher, 'author': book.author}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], publisher = request.json['publisher'], author = request.json['author'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return{"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return{"message": "deleted"}

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if book is None:
        return{"error": "not found"}
    book = Book(book_name=request.json['book_name'], publisher = request.json['publisher'], author = request.json['author'])
   
    db.session.commit()
    return{"message": "updated"}