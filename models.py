from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Form(db.Model):
    __tablename__ ="form"
    username      = db.Column(db.String,primary_key=True)
    password      = db.Column(db.String)
    TimeStamp     = db.Column(db.DateTime)


    def __init__(self, username,password,TimeStamp):
        self.username   = username
        self.password   = password
        self.TimeStamp  = TimeStamp
    
    
    
    
    def print(self):
        return self.username


class Books(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    year = db.Column(db.String)

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        return self.title


class Reviews(db.Model):
    __tablename__ ="reviews"
    __table_args__ = (db.PrimaryKeyConstraint('isbn', 'username'),)
    isbn         =   db.Column(db.String, db.ForeignKey('books.isbn'))
    username     =   db.Column(db.String, db.ForeignKey('form.username'))
    review       =   db.Column(db.String)
    rating       =   db.Column(db.Integer)

    def __init__(self, isbn, username, review, rating):
        self.isbn       = isbn
        self.username   = username
        self.review    = review
        self.rating  = rating

    
    def __repr__(self):
        return self.isbn+" : "+self.username+" : "+self.review+" : "+str(self.rating)