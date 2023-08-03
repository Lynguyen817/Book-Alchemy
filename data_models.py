from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine, Column, Integer, String, Date
# from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

# engine = create_engine('sqlite:///data/library.sqlite')
# Session = sessionmaker(bind=engine)
# session = Session()


class Author(db.Model):
    __tablename__= 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date)

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}', birth_date='{self.birth_date}', date_of_death='{self.date_of_death}')"

    def __str__(self):
        return f"Author: {self.name}"


author = Author(
    id=1,
    name="Sir Arthur Conan Doyle",
    birth_date=1859,
    date_of_death=1930
)


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship(Author, backref=db.backref('books'))

    def __repr__(self):
        return f"Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', publication_year={self.publication_year}, author_id={self.author_id})"

    def __str__(self):
        return f"Book: {self.title} ({self.publication_year})"


book = Book(
    id=10,
    isbn=20,
    title="Sherlock Holmes",
    publication_year=1887,
    author_id=1,
    author=Author(name="Sir Arthur Conan Doyle")
)
#db.create_all()