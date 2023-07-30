from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from data_models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'

db = SQLAlchemy()
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        bio = request.form['bio']

        author = Author(name=name, bio=bio)
        db.session.add(author)
        db.session.commit()

        return render_template('add_author.html', success=True)
    else:
        return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author']

        book = Book(title=title, author_id=author_id)
        db.session.add(book)
        db.session.commit()

        return render_template('add_book.html', success=True)
    else:
        return render_template('add_book.html')


@app.route('/book/<int:book_id>/delete', method=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    author_id = book.author_id
    db.session.delete(book)
    db.session.commit()

    # Check if the author has any other books in the library
    author = Author.query.get_or_404(author_id)
    if not author.books:
        db.session.delete(author)
        db.session.commit()


@app.route('/')
def home():
    # Query the Book table for all books
    books = Book.query.all()
    formatted_books = [{'title': book.title, 'author': book.author} for book in books]
    return render_template('home.html', books=formatted_books)


if __name__ == "__main__":
    app.run(debug=True)