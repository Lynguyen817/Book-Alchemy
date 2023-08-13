from flask import Flask, render_template, request, redirect
from data_models import *
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birthdate_str = request.form['birthdate']
        date_of_death_str = request.form['date_of_death']

        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date() if birthdate_str else None
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

        author = Author(name=name, birthdate=birthdate, date_of_death=date_of_death)
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


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)

        author_id = book.author_id
        db.session.delete(book)
        db.session.commit()

        # Check if the author has any other books in the library
        author = Author.query.get_or_404(author_id)
        if not author.books:
            db.session.delete(author)
            db.session.commit()

        return redirect('/')
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/')
def home():
    # Query the Book table for all books
    books = Book.query.all()
    formatted_books = [{'title': book.title, 'author': book.author} for book in books]
    return render_template('home.html', books=formatted_books)


if __name__ == "__main__":
    app.run(debug=True)
