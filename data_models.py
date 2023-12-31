from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """ Creates an authors table with columns of id, name, birthdate and date of death"""
    __tablename__= 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date)

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}', birth_date='{self.birth_date}', date_of_death='{self.date_of_death}')"

    def __str__(self):
        return f"Author: {self.name}"


class Book(db.Model):
    """ Creates a books table that has columns of id, isbn, title,publication-year, author-id.
        ForeignKey is author-id.
    """
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship(Author, backref=db.backref('books'))

    def __repr__(self):
        return f"Book(id={self.id}, isbn='{self.isbn}', title='{self.title}',publication_year={self.publication_year},.\
          author_id={self.author_id})"

    def __str__(self):
        return f"Book: {self.title} ({self.publication_year})"


