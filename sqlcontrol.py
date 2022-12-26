import mysql.connector
f=mysql.connector.connect(host='localhost', user='ananya', password='home123', database='lms')
cursor=f.cursor(buffered=True)
def checkifexistsid(column, table,id):
    s="select {} from {} where {}={}".format(column,table,column,id)
    cursor.execute(s)
    b=cursor.fetchall()
    if b==[]:
       return("None")
    else:
       return("Yes")
def checkifexistsname(column, table, name):
   s="select {} from {} where {}='{}'".format(column,table,column,name)
   cursor.execute(s)
   b=cursor.fetchall()
   if b==[]:
       return("None")
   else:
       return("Yes")
def signup(username, password, emailid):
   if checkifexistsname('username', 'ruser', username)=='None':
       userid=idcreate("userid","ruser")
       s="insert into ruser(username, rpassword, emailid, userid) values('{}','{}','{}',{})".format(username, password, emailid, userid)
       cursor.execute(s)
       f.commit()
       return 'success'
   else:
       return("Not")
def passwordcheck(username,password):
   s="select rpassword from ruser where username='{}'".format(username,)
   cursor.execute(s)
   c=cursor.fetchall()
   for k in c:
       if k[0]==password:
           return("Success")
def signincheck(username,password):
    c=checkifexistsname('username', 'ruser', username)
    if c=='Yes':
       d=passwordcheck(username,password)
       if d=='Success':
            return("Success")
       else:
            return("Incorrect password")
    else:
        return("Incorrect username.")

#idcrud  
def idcreate(column,table):
    #returns id
   s="select max({}) from {}".format(column,table)
   cursor.execute(s)
   a=cursor.fetchone()
   for r in a:
       if r==None:
           r=0
       r+=1
       return r
def iddelete(idcolumn, table, id):
    #returns None
    s="delete from {} where {}={}".format(table,idcolumn,id)
    cursor.execute(s)
    f.commit()
def idupdate(idcolumn, table, id,newid):
    #returns None
    s="update {} set {}={} where {}={}".format(table,idcolumn,newid,idcolumn,id)
    cursor.execute(s)
    f.commit()
def idsread(idcolumn,table):
    #Returns list
    s='select {} from {}'.format(idcolumn,table)
    cursor.execute(s)
    a=cursor.fetchall()
    b=[]
    for r in a:
        b.append(a[0])
    return b
def stringupdate(column,idcolumn, id, newname,table):
    s='update {} set {}={} where {}={}'.format(table,column,newname,idcolumn,id)
    cursor.update(s)
    f.commit()
 
#selectby. Be clear. Authorname is not unique. Double selection required. column1 is what has to be searched and column to is what you search with
def selectbydigit(constraint,column1,column2,table):
    s="select {} from {} where {}={}".format(column1,table, column2,constraint)
    cursor.execute(s)
    a=cursor.fetchall()
    for r in a:
       return(r[0])
def selectbyname(column1, table, column2, constraint):
    s="select {} from {} where {}='{}'".format(column1,table, column2,constraint)
    cursor.execute(s)
    a=cursor.fetchall()
    for r in a:
       return(r[0])
 
#insertion into tables Returns none
def insertauthor(userid,authorname):
   authorid=idcreate("authorid","author")
   s="insert into author values({},'{}')".format(authorid, authorname)
   cursor.execute(s)
   f.commit()
   s="update ruser set authorid={} where userid={}".format(authorid,userid)
   cursor.execute(s)
   f.commit()
def insertchapter(bookid, chapternumber, chaptertitle, content):
   chapterid=idcreate("chapterid","chapter")
   s="insert into chapter values({}, {}, {}, '{}','{}')".format(chapterid, bookid, chapternumber, chaptertitle, content)
   cursor.execute(s)
   f.commit()
def insertbook(bookname,summary,authorid):
   bookid=idcreate("bookid",'book')
   s="insert into book(bookid, bookname, summary) values({},'{}','{}')".format(bookid,bookname,summary)
   cursor.execute(s)
   f.commit()
   insertauthorbook(bookid, authorid)
def insertgenre(genre):
   if checkifexistsname('genre','genre',genre)!="None":
       return("Genre exists.")
   genreid=idcreate('genreid','genre')
   s="insert into genre values({},'{}')".format(genreid, genre)
   cursor.execute(s)
   f.commit()
def insertauthorbook(bookid,authorid):
   authorbookid=idcreate('authorbookid','authorbook')
   s="insert into authorbook values({},{},{})".format(authorbookid,bookid,authorid)
   cursor.execute(s)
   f.commit()
def insertbookgenre(genreid,bookid):
   bookgenreid=idcreate('bookgenreid','bookgenre')
   s="insert into bookgenre values({},{},{},{})".format(bookgenreid,genreid,bookid)
   cursor.execute(s)
   f.commit()
def insertuserbook(bookid, userid):
    userbookid=idcreate('userbookid', 'userbook')
    s="insert into userbook values({},{},{},{})".format(userbookid, bookid, userid,0)
    cursor.execute(s)
    f.commit()
def insertcommented(userid,chapterid,bookid,commento,content):
    commentid=idcreate('commentid', 'commented')
    s="insert into commented values({},{},{},{},{},'{}')".format(commentid,userid,chapterid,bookid,commento,content)
    cursor.execute(s)
    f.commit()
def insertrating(bookid, newrating):
    rating=selectbydigit(bookid,'rating','bookid', 'rating')
    ratingid=idcreate('ratingid', 'rating')
    s="select people from rating where bookid={}".format(bookid)
    cursor.execute(s)
    a=cursor.fetchone()
    rating+=float(newrating)
    people=a[0]+1
    if a==None:
        people=1
        s="insert into rating values({},{},{},{})".format(ratingid, bookid, rating,people)
    else:
        s='update rating set rating={} where bookid={}'.format(rating, bookid)
        cursor.execute(s)
        f.commit()
        s='update rating set people = people + 1 where bookid={}'.format(bookid,)
    cursor.execute(s)
    f.commit()
    b=rating/people
    s="update book set rating={} where bookid={}".format(b, bookid)
    cursor.execute(s)
    f.commit()
 
#Selecting all books by an id (For library). Returns list
def selectall(idcolumn,column,table,theid):
    s="select {} from {} where {}={}".format(column, table, idcolumn,theid)
    cursor.execute(s)
    a=cursor.fetchall()
    l=[]
    for r in a:
        l.append(r[0])
    return l
 
#Returns ids
def searchidlikename(column, idcolumn, table,word):
    s="select {} from {} where {} like '%{}%'".format(idcolumn, table, column, word)
    cursor.execute(s)
    a=cursor.fetchall()
    l=[]
    for r in a:
        l.append(r)  
    return l
def searchbook(word):
    #book
    booklist=searchidlikename('bookname', 'bookid', 'book', word)
    return(booklist)
    #genre
    genrelist=searchidlikename('genre', 'genreid', 'genre', word)
    bookgenrelist=[]
    for r in genrelist:
        a=selectbydigit(r[0],'bookid', 'genreid', 'bookgenre')
        bookgenrelist.append(a)
    list2=[]
    for r,i in zip(bookgenrelist, genrelist):
        list2.append([r,i])
    a=[]
    for r in list2:
        if a==[]:
            a.append(r)
        else:
            for i in a:
                if r[0] in i:
                    x=r.pop(0)
                    i.extend(r)
                    break
            else:
                a.append(r)
    for r in a:
        if r[0] in booklist:
            booklist.remove(r[0])
    booklist.extend(a)
    return(booklist)
def searchauthor(word):
     authorlist=searchidlikename('authorname','authorid', 'author', word)
     l=[]
     for r in authorlist:
       l.append(r[0])
     return l
def listtohyper(list,dir):
   a=''
   for r in list:
       r=str(r)
       b=r.replace(' ','_')
       a+='<p><a href="'+dir+'/'+b+'">'+r+'</a></p> '
   return (a)
def selectallbooks():
   s='select bookname, authorname from book, authorbook, author where book.bookid=authorbook.bookid and author.authorid=authorbook.authorid;'
   cursor.execute(s)
   a=cursor.fetchall()
   return a
def bookshyper(books,author,dir='/book'):
   c=''
   for r in range(len(books)):
       a=str(books[r])
       b=a.replace(' ','_')
       d=author[r].replace(' ','_')
       c+='<p><a href="'+dir+'/'+d+'/'+b+'">'+books[r]+'</a>, '+ author[r]+'</p> '
   return c
def selectrating(authorname, bookname):
   bookname=bookname.replace('_',' ')
   s='select rating from book, authorbook, author where book.bookid=authorbook.bookid and authorbook.authorid=author.authorid and authorname="{}" and bookname="{}"'.format(authorname,bookname)
   cursor.execute(s)
   a=cursor.fetchone()
   b=str(a[0])
   return b
 
def selectgenre(bookname,authorname):
    s='select book.bookid from book,authorbook, author where author.authorid=authorbook.authorid and book.bookid=authorbook.bookid and authorname="{}" and bookname="{}"'.format(authorname, bookname)
    cursor.execute(s)
    a=cursor.fetchall()
    print(a)
    if a==[]:
        return 'None'
    else:
        a=a[0][0]
    s='select genre from genre, book, bookgenre where genre.genreid=bookgenre.genreid and book.bookid=bookgenre.bookid and book.bookid={}'.format(a,)
    cursor.execute(s)
    a=cursor.fetchall()

    l=[]
    for r in a:
        l.append(r[0])
    return l
def listtocomma(list, dir):
    a=''
    for r in list:
       r=str(r)
       b=r.replace(' ','_')
       a+=' <a href="'+dir+'/'+b+'">'+r+'</a> '
    return a
def selectchapters(bookname,authorname):
    a=bookid(bookname, authorname)
    s='select chapternumber, chaptertitle from chapter,book where chapter.bookid=book.bookid and book.bookid={}'.format(a)
    cursor.execute(s)
    b=cursor.fetchall()
    return b
def selectchapter(bookname,authorname,chapternumber):
    s='select chapternumber, chaptertitle from chapter, book, author, authorbook where chapter.bookid=book.bookid and author.authorid=authorbook.authorid and book.bookid=authorbook.bookid and bookname="{}" and authorname="{}" and chapternumber={}'.format(bookname,authorname,chapternumber)
    cursor.execute(s)
    a=cursor.fetchall()
    if a==[]:
        a='No chapters yet.'
    return a
def hyperchapter(list,livre):
    if list=='No chapters yet.':
        return list
    c=''
    for r in list:
       e=str(r[0])
       c+='<p><a href="/book/'+livre+'/'+e +'">'+e+'    '+r[1]+'</a></p> '
    return c
def hyperchapbook(bookname,a,livre):
    c='<p><a href="/book/'+livre+'">'+bookname+'</a></p><p>Chapter '+a[0]+'</p><p>'+a[1]+'</p><p>'+a[2]
    return c
def bookid(bookname, authorname):
    s='select book.bookid from author,book,authorbook where authorbook.authorid=author.authorid and book.bookid=authorbook.bookid and authorname="{}" and bookname="{}"'.format(authorname, bookname)
    cursor.execute(s)
    a=cursor.fetchone()
    return a[0]
def selectsummary(bookname):
    s='select summary from book where bookname="{}"'.format(bookname,)
    cursor.execute(s)
    a=cursor.fetchone()
    return(a[0])
def selectimageurl(bookname):
    s='select imageurl from book where bookname="{}"'.format(bookname,)
    cursor.execute(s)
    a=cursor.fetchone()
    return(a[0])
def selectuserbook(username,bookname,authorname):
    a=bookid(bookname,authorname)
    b=selectbyname('userid','ruser','username',username)
    c='select * from userbook where bookid={} and userid={}'.format(a,b)
    cursor.execute(c)
    a=cursor.fetchall()
    return a
def deleteuserbook(username,bookname,authorname):
    a=bookid(bookname,authorname)
    b=selectbyname('userid','ruser','username',username)
    s='delete from userbook where userid={} and bookid={}'.format(b,a)
    cursor.execute(s)
    f.commit()
def library(username):
    a=selectbyname('userid','ruser','username',username)
    s='select bookname, authorname from book, authorbook, userbook, author where userbook.bookid=book.bookid and authorbook.bookid=book.bookid and author.authorid=authorbook.authorid and userid={}'.format(a,)
    cursor.execute(s)
    a=cursor.fetchall()
    return a
