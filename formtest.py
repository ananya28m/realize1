# importing Flask and other modules
from flask import Flask, request, render_template, redirect, session
from flask_bootstrap import Bootstrap
import sqlcontrol
from flask_session import Session
# Flask constructor
 
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
Bootstrap(app)
# A decorator used to tell the application
# which URL is associated function
@app.route("/")
def home():
   if not session.get("username"):
       return redirect('/signin')
   else:
       return redirect('/book')
@app.route('/library')
def library():
   if not session.get("username"):
       return redirect('/')
   else:    
       a=sqlcontrol.library(session['username'])
       if a != []:
        d={}
        for r in a:
            d[r[0]]=r[1]
        return render_template('books.html', dictionary=d, title='My Library')
       else:
        return render_template('nobooks.html',title='My Library',library='Add books using the "Add to library" button.')
 
@app.route('/signin', methods =["GET", "POST"])
def signin():
   if request.method == "POST":
       username=request.form.get("username")
       password=request.form.get("password")
       # print(sqlcontrol.signincheck(username,password))
       if sqlcontrol.signincheck(username,password)=='Success':
           session["username"] = username
           return redirect('/')
       elif sqlcontrol.signincheck(username,password)=='Incorrect password':
           return('<p><h1>Password is incorrect.</h1></p><p><h1><a href="/signin">Retry</a></h1><p>')
       elif sqlcontrol.signincheck(username,password)=='Incorrect username':
           return('<p><h1>Username is incorrect.</h1></p><p><h1><a href="/signin">Retry</a></h1><p>')
   return render_template('signin.html')    
 
@app.route('/signout')
def signout():
   session['username']=None
   return redirect('/')
 
@app.route('/signup', methods =["GET", "POST"])
def gfg():
   if request.method == "POST":
       username=request.form.get("username")
       password=request.form.get("password")
       emailid=request.form.get("emailid")
       a=sqlcontrol.signup(username, password, emailid)
       if a=='success':
           session["username"] = username
           return redirect('/book')
       elif a=='Not':
           return render_template("usernameexists.html")
   return render_template('signup.html')
@app.route('/recommend')
def recommend():
   return 'i recommend'
 
@app.route('/book')
def books():
    a=sqlcontrol.selectallbooks()
    if a != []:
        d={}
        for r in a:
            d[r[0]]=r[1]
        return render_template('books.html', dictionary=d, title='All Books')
    else:
        return render_template('nobooks.html',title='All Books',library="There are no books yet.")

@app.route('/book/<author>/<livre>')
def livres(author,livre):
    book=livre.replace('_', ' ')
    author1=author.replace('_', ' ')
    b=sqlcontrol.selectrating(author1, book)
    rating=str(b)
    genrelist=sqlcontrol.selectgenre(book,author1)
    chapterslist=sqlcontrol.selectchapters(book,author1)
    d={}
    for r in chapterslist:
        d[r[0]]=r[1]
    summary=sqlcontrol.selectsummary(book)
    imageurl=sqlcontrol.selectimageurl(book)
    if sqlcontrol.selectuserbook(session["username"],book, author1)==[]:
        return render_template('showbookfollow.html',book=book, author=author1, rating=rating, summary=summary, imageurl=imageurl,genrelist=genrelist, dictionary=d)
    else:
        return render_template('showbookdefollow.html',book=book, author=author1, rating=rating, summary=summary, imageurl=imageurl,genrelist=genrelist, dictionary=d)

@app.route('/rating/<author>/<livre>', methods =["GET", "POST"])
def rating(author, livre):
    book=livre.replace('_',' ')
    print(book)
    i=sqlcontrol.selectimageurl(book)
    if request.method == "POST":
        rating=request.form.get("rating")
        newrating=rating
        book=livre.replace('_',' ')
        author1=author.replace('_', ' ')
        bookid=sqlcontrol.bookid(book,author1)
        sqlcontrol.insertrating(bookid,newrating)
        return redirect('/book/'+author+'/'+livre)
    return render_template('rating.html', livre=livre, author=author, book=livre.replace('_'," "), i=i)
    
@app.route('/book/<author>/<livre>/<chapternumber>/chaptertitle')
def book(livre, author, chapternumber, chaptertitle):
    book=livre.replace('_', ' ')
    author1=author.replace('_', ' ')
    a=sqlcontrol.selectchapter(book,author1,chapternumber)
    return a
@app.route('/search')
def search():
   return'<p><h1>Search RealiZe</h1></p> <p><h2> <a href="/authorsearch">Search by Author</a></h2></p> <p><h2><a href="/booksearch">Search by book or genre</a></h2></p>'
 
@app.route('/authorsearch', methods =["GET", "POST"])
def authorsearch():
   if request.method == 'POST':
       search=request.form.get("search")
       a=sqlcontrol.searchauthor(search)
       c=[]
       for r in a:
           b=sqlcontrol.selectbydigit(r,'authorname','authorid','author')
           c.append(b)
       return render_template('authorresults.html', authorlist=c)
   return render_template('authorsearch.html')  
 
@app.route('/author/<authorname>')
def author(authorname):
   author1=authorname.replace('_', ' ')
   c=sqlcontrol.selectbyname('authorid','author','authorname',author1)
   b=sqlcontrol.selectall('bookid','authorid','authorbook',c)
   if b==[]:
    d='<p>There are no books yet.</p>'
   else:
        l=[]
        for r in b:
            l.append(sqlcontrol.selectbydigit(r, 'bookname','bookid', 'book'))
        d=sqlcontrol.listtohyper(l,'/book/'+authorname)
   a='<p><h1>%s</h1></p> <p>Books</p>'+d
   return a%authorname
'''@app.route('/booksearch')
def booksearch():
   if request.method == 'POST':
       search=request.form.get("search")
       a=sqlcontrol.searchbook(search)
       c=[]
       for r in a:
           b=sqlcontrol.selectbydigit(r,'authorname','authorid','author')
           c.append(b)
       return render_template('authorresults.html', authorlist=c)
   return render_template('authorsearch.html')  '''
@app.route('/follow/<author>/<livre>')
def follow(author,livre):
    book=livre.replace('_', ' ')
    author1=author.replace('_', ' ')
    a=sqlcontrol.bookid(book,author1)
    b=sqlcontrol.selectbyname('userid','ruser','username',session['username'])
    sqlcontrol.insertuserbook(a,b)
    return redirect('/book/'+author+'/'+livre)
@app.route('/defollow/<author>/<livre>')
def defollow(author,livre):
    book=livre.replace('_', ' ')
    author1=author.replace('_', ' ')
    sqlcontrol.deleteuserbook(session['username'],book,author1)
    return redirect('/book/'+author+'/'+livre)


#if __name__ == '__main__':
  #  app.run(debug=True)

