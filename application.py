import os
import datetime
from flask import Flask, session,render_template,request,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine,and_,or_
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify
from models import *
from sqlalchemy import text

app = Flask(__name__)   
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# db.init_app(app)
Session(app)
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return "Project 1: TODO"

@app.route('/register/<int:args>', methods=['post','get'])
@app.route('/register/', methods=['post', 'get'])
def register(args=None):
    message = ''
    if request.method == 'POST':
        if args == None:
            username = request.form.get('username')  # access the data inside 
            password = request.form.get('password')
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>{username}, : {password}")
            if len(username)<1 or len(password)<1:
                message = "UserName and password Can't be Empty"
            elif db.query(Form).get(username) is not None:
                message = "UserName Already Registered "
            else:
                message  = username + " , Your account has been registered successfully  "
                TimeStamp = datetime.datetime.now()
                form = Form(username,password,TimeStamp)
                db.add(form)
                db.commit()
            return render_template('Form.html', message=message)
            
    else:    #i.e If accessed directly via url(i.e GET)
        if args==1:
            return render_template('Form.html',message="Please Enter Valid Password")


        elif args==2:
            return render_template('Form.html',message="Please Enter Valid Credentials")


        elif args==3:
            return render_template('Form.html',message="Session Expired")


        elif args==4:
            return render_template('Form.html',message="Logged Out Successfully")

        
        elif args==5:
            return render_template('Form.html',message="Not Allowed !!! Log In First")

        else :
            return render_template('Form.html')


@app.route('/admin')
def admin():
    x = db.query(Form).order_by(Form.TimeStamp)
    return render_template("admin.html",list = x)

@app.route('/auth',methods=['post','get'])
def auth():
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        form    = db.query(Form).get(username)
        try:
            if(username==form.username) and (password==form.password):
                # session['user'] = form
                return redirect(url_for('home'))
            else:
                return redirect(url_for('register',args=1))
        except:
            return redirect(url_for('register',args=2))
            
    else:
        return redirect(url_for('register',args=5))


@app.route('/home')
def home():
    try:
        Username =session['user'].username
        return render_template('change.html',username=Username)
    except:
        return redirect(url_for('register',args=3))
        

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('register',args=4))

@app.route('/login')
def login():
    return redirect('search')

@app.route('/book/<string:args>')      
@app.route('/book')
def book(args=None):
    isbn = args
    list = db.query(Books).filter(Books.isbn==isbn).all()
    obj = ""
    for x in list:
        if x.isbn==isbn:
            print(isbn)
            obj = x
            break

    print(f"ISBN :{isbn} , Username :{session['user'].username}")
    rev= db.query(Reviews).filter(and_(Reviews.username == session['user'].username, Reviews.isbn == isbn)).first()
    message=""

    print(f"obj :{obj}")

    if rev is  not None:
        rate=rev.rating
        comment=rev.review
        message="you have already submitted review for this book"
        reviews=db.query(Reviews).filter(Reviews.isbn==isbn).all()
        return render_template('bookpage.html',username=session['user'].username,obj=obj, message=message, Rating=rate, Review=comment,reviews=reviews)
    else:
        message="please submit review"
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Rev None")
        return render_template('bookpage.html',username=session['user'].username, obj=obj,message=message,Rating=None,Review=None)

@app.route('/review/<string:name>')
@app.route('/review', methods=['post'])
def review(name=None):
    Rating=request.form.get('Rating')
    Review=request.form.get('Review')
    print(f"Rating : {Rating}")
    print(f"Review :{Review}")
    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> , Username :{session['user'].username}")
    list = db.query(Books).filter(Books.isbn==request.form.get("ISBN")).all()
    print(type(list))
    obj = ""
    for x in list:
        if x.isbn==request.form.get("ISBN"):
            obj = x
            break

    reviews=db.query(Reviews).filter(Reviews.isbn=="0765317508").all()
    print(type(reviews))

    reviews = Reviews(username=session['user'].username, isbn=request.form.get("ISBN"), review=Review, rating=Rating)
    try:
        db.add(reviews)
        db.commit()
        message="successfully submitted your review"
        reviews=db.query(Reviews).filter(Reviews.isbn==request.form.get("ISBN")).all()
        return render_template('book.html',username=session['user'].username, message=message,obj=obj,reviews=reviews)

    except:
        message="You have already submitted your review"
        reviews=db.query(Reviews).filter(Reviews.isbn==request.form.get("ISBN")).all()
        return render_template('book.html',username=session['user'].username, message=message,obj=obj,reviews=reviews)


@app.route('/search',methods=['post','get'])
def search():
    try:
        session['user'].username
    except:
        return redirect(url_for('register',args=3))
    if request.method == 'POST':
        Field=((request.form['Choose Field']))
        print(f"Field :  {Field} ")
        Key = request.form.get('Search Bar')
        search = "%{}%".format(Key)

        if Field == "title" :

            list = db.query(Books).filter(Books.title.like(search))
            count = 0
            for x in list:
                print(x)
                count=count+1
            return render_template('search.html',list=list,length=count,username=session['user'].username)


        elif Field == "isbn" :

            list = db.query(Books).filter(Books.isbn.like(search))
            count = 0
            for x in list:
                print(x)
                count=count+1
            return render_template('search.html',list=list,length=count,username=session['user'].username)

        elif Field == "author" :

            list = db.query(Books).filter(Books.author.like(search))
            count = 0
            for x in list:
                print(x)
                count=count+1
            return render_template('search.html',list=list,length=count,username=session['user'].username)

        else :
            key = "{}%".format(Key)
            list = db.query(Books).filter(Books.year.like(key))
            count = 0
            for x in list:
                print(x)
                count=count+1
            return render_template('search.html',list=list,length=count,username=session['user'].username)

    else:
        return render_template('search.html',length=-1,username=session['user'].username)



@app.route('/api/<string:args>')      
@app.route('/api')
def api(args=None):
    # obj = db.query(Books).filter(Books.isbn==args).first()
    obj = db.query(Books).filter(or_(Book.ISBN.like(args), Book.year.like(args), Book.author.like(args), Book.title.like(args))).all()
    print(obj)
    return jsonify(isbn= obj.isbn
    ,title = obj.title,
        author = obj.author
        ,year = obj.year)

@app.route('/api/search',methods=['post','get'])
def searchapi():
    args = request.form.get('search_input')
    print(args)
    args = "%{}%".format(args)
    args = args.title()
    obj = db.query(Books).filter(or_(Books.isbn.like(args), Books.year.like(args), Books.author.like(args), Books.title.like(args))).all()

    books={"books_1":[]}
    for x in obj:
         element = dict()
         element["ISBN"] = x.isbn
         element["Title"] = x.title
         element["Author"] = x.author
         element["Year"] = x.year
         books["books_1"].append(element)
    if len(obj)>0:
        books["success"]=True
        # print(books)
        return jsonify(books)
    else:
        return jsonify({"success": False})