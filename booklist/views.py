from django.http import HttpResponse
from django.http import HttpRequest

from django.template import RequestContext
from django.shortcuts import render,render_to_response

# import datetime
from .models import Book,Note,Blog,BookList,MyUser

# import logging

from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

from datetime import datetime,date
from itertools import chain

from django.utils.log import logging
logger = logging.getLogger('django.request')

# Create your views here.

# def index2(request):
# 	now = datetime.datetime.now()
# 	html = "<html><body>It is now %s. by frank</body></html>" % now
# 	return HttpResponse(html)

def calculateAgeDays(year,month,day):
    now = date.today()
    birthday = date(int(year),int(month),int(day))
    age = now-birthday
    return age.days

def other(request):
    if request.method=='POST':
        form = BirthdayForm(request.POST)
        year = request.POST['year']
        month = request.POST['month']
        day = request.POST['day']
        

        if int(year)==0 or int(month)==0 or int(day)==0:
            return render(request,'booklist/other.html',{'form':form,'text':"year.month.day !=0"})
        days = calculateAgeDays(year,month,day)

        return render(request,'booklist/other.html', {
            "form":form,
            "days":days,
            "text":"now = %s"%date.today(),
            "username":'xi',
            "qq":'394813654',
            "weixin":'xixiaohui2011',
            "address":"hefei anhui."
            })
    else:
        form = BirthdayForm()
        return render(request,'booklist/other.html', {
            "form":form,
            "text":"now = %s"%date.today(),
            "username":'xi',
            "qq":'394813654',
            "weixin":'xixiaohui2011',
            "address":"hefei anhui."
            })

def index(request):
    booklists = BookList.objects.all()

    return render(request,'booklist/index.html', {
        'booklists':booklists,
        })

def books(request):
    """Renders the mybookhome page."""
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated():
        return mylogin(request)

    if request.user.is_authenticated():
        username = request.user.get_username()
        books = Book.objects.filter(user=request.user)

        myuser = MyUser.objects.get(user=request.user)
        # friends = myuser.getFriend()
        friends = myuser.privatef_set.all()

        friendsBooks = Book.objects.none()
        for friend in friends.all():
            friendbooks = Book.objects.filter(user=friend.getUser())
            friendsBooks = friendsBooks | friendbooks

        # for item in friendsBooks:            
        #     logger.debug(item)
    else:
        username = '?'
        books = None
        friendsBooks = None
     
    return render(
        request,
        'booklist/books.html',
        context_instance = RequestContext(request,
        {
            'books':books,
            'username':username,
            'friends':friends,
            'friendsBooks':friendsBooks,
        })
    )

def tourist_bookin(request):
        bookname = request.GET.get('bookname')
        book = Book.objects.filter(name=bookname)[0]
        bookNotes = book.notes.all()

        return render(request,'booklist/bookin.html', {
            'book':book,
            'bookNotes':bookNotes,
            'lock':False,
            })    

def bookin(request):
    if not request.user.is_authenticated():
        return mylogin(request)

    if request.method == 'POST':
        noteForm = NoteForm(request.POST)

        if noteForm.is_valid():
            time = datetime.today()
            text = request.POST['text']
            # book = Book.objects.filter(name = bookname)[0]
            bookname = request.GET.get('bookname')
            book = Book.objects.get(name=bookname)

            # logger.error('text=%s' % (text))
            note = Note.objects.create_note(time,text,book)
            note.setBook(book)
            note.save()

            bookNotes = book.notes.all()
            
            # logger.error("1%s"%book)
            # logger.error(bookNotes)

            return render(request,'booklist/bookin.html', {
                'book':book,
                'form':noteForm,
                'bookNotes':bookNotes,
                'lock':request.user.is_authenticated(),
                })
            # return render_to_response('booklist/success.html',{'title':'AddNote success!',})
    else:
        bookname = request.GET.get('bookname')
        book = Book.objects.get(name=bookname)
        bookNotes = book.notes.all()

        # logger.error("2%s"%book)
        # logger.error(bookNotes)

    	return render(request,'booklist/bookin.html', {
            'book':book,
            'form':NoteForm(),
            'bookNotes':bookNotes,
            'lock':request.user.is_authenticated(),
            })

def mylogin(request):
    if request.method == 'POST':
        logform = LogInForm(request.POST)
        if logform.is_valid():
            
            # username=logform.cleaned_data['name']
            # password=logform.cleaned_data['word']
            username = request.POST['name']
            password = request.POST['word']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request,'booklist/success.html',{'title':'Login success!', })
                    # Redirect to a success page.
                # else:
                    # Return a 'disabled account' error message
                    # ...
    else:
        logform = LogInForm()
    return render(request,'booklist/login.html',{
        'form':logform,
        'user':request.user,
        })      

def register(request):
    if request.method=='POST':
        # data = {'username': 'hello',
        #         'password': '123',
        #         'email': 'foo@example.com',}
        f = RegisterForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            email = f.cleaned_data['email']
            #create User
            user = User.objects.create_user(username=username,password=password,email=email)
            user.save()

            myuser = MyUser.objects.create(user=user)
            myuser.save()


            return render(request,'booklist/login.html',{
                'form':LogInForm(),
                })
        else:
            return render(request,'booklist/register.html',{
                'form':f,
                })
    else:
        form = RegisterForm()    
        return render(request,'booklist/register.html',{
            'form':form,
            })

def logout_view(request):
    logout(request)
    return render(request,'booklist/success.html',{'title':'LogOut success!',})


def addBook(request):
    if not request.user.is_authenticated():
        return mylogin(request)

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            name = form.cleaned_data['name']
            author = form.cleaned_data['author']
            publish = form.cleaned_data['publish']
            date = form.cleaned_data['date']
            isbn= form.cleaned_data['ISBN13']
            summary = form.cleaned_data['summary']

            book = Book.objects.create_book(name,author,publish,date,isbn,request.user,summary)
            book.setUser(request.user)
            book.save()

            return render_to_response('booklist/success.html',{'title':'AddBook success!', })
    else:
        form = BookForm()
    return render(request,'booklist/addbook.html',{'form':form})

def success(request):
    return render_to_response('booklist/success.html',{})

def minus(request):

    if not request.user.is_authenticated():
        return mylogin(request)

    name = request.GET.get('bookname')
    book = Book.objects.filter(name=name)
    book.delete()
    return render_to_response('booklist/success.html',{'title':'MinusBook success!', })

def addNote(request):
    return render_to_response('booklist/success.html',{'title':'AddNote success!', })

def rmnote(request):
    pk = request.GET.get('pk')
    note = Note.objects.filter(pk=pk)
    note.delete()
    return render_to_response('booklist/success.html',{'title':'Remove Note success!', })

def addBlog(request):
    if not request.user.is_authenticated():
        return mylogin(request)
    else:
        blogs = Blog.objects.filter(user=request.user)
    # blogs = Blog.objects.all()

    if request.method=='POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            # logger.debug(title)
            # logger.debug(text)
            blog = Blog.objects.create(title=title,text=text)
            blog.setUser(request.user)
            blog.save()
            return render(request,'booklist/blog.html',{
            'form':form,
            'blogs':blogs,
            'username':request.user.get_username(),
            })
    else:    
        form = BlogForm()
        return render(request,'booklist/blog.html',{
            'form':form,
            'blogs':blogs,
            'username':request.user.get_username(),
            })

def rmBlog(request):
    title = request.GET.get('title')
    blog = Blog.objects.filter(title=title)
    blog.delete()
    return render_to_response('booklist/success.html',{'title':'Remove Blog success!', })

def zodiac(request):
    if request.method=='POST':
        zodiacForm = ZodiacForm(request.POST)
        if zodiacForm.is_valid():
            date = form.cleaned_data['date']

        return render(request,'booklist/zodiac.html',{
            'zodiacForm':zodiacForm,
            })
    else:    
        zodiacForm = ZodiacForm()
        return render(request,'booklist/zodiac.html',{
            'zodiacForm':zodiacForm,
            })

def allBooks(request):
    allbooks = Book.objects.all()

    return render(request,'booklist/allbooks.html',{
        'allbooks':allbooks,

        })

def addbooklist(request):
    if not request.user.is_authenticated():
        return mylogin(request)

    if request.method=='POST':
        form = BookListForm(request.POST)
        form.setBooksQueryset(Book.objects.filter(user=request.user))

        if form.is_valid():
            title = form.cleaned_data['title']
            introduce = form.cleaned_data['introduce']
            books = form.cleaned_data['books']
            logger.debug(books)
            
            newbooklist = BookList.objects.create(title=title,introduce=introduce,user=request.user)
            for book in books:
                newbooklist.addBook(book)
                # logger.debug(book.name)

            newbooklist.save()

            return render(request,'booklist/success.html',{'title':'Create NewBookList Success!'})
    else:
        books = Book.objects.filter(user=request.user)
        form = BookListForm()
        form.setBooksQueryset(books)
        
        allBookLists = BookList.objects.filter(user=request.user)

        myuser=MyUser.objects.get(user=request.user)
        privateFriends = myuser.privatef_set.all()
        for friend in privateFriends:
            privateFriendBooklist = BookList.objects.filter(user=friend.getUser())
            allBookLists = allBookLists | privateFriendBooklist

        return render(request,'booklist/addbooklist.html',{
            'form':form,
            'allBookLists':allBookLists,

            })

def allbooklist(request):
    allBookLists = BookList.objects.all()

    return render(request,'booklist/allbooklist.html',{
        'allBookLists':allBookLists,
        })

def searchBooklist(request):
    search = request.GET.get('search')
    searchbooklist = BookList.objects.filter(title__icontains=search)

    return render(request,'booklist/allbooklist.html',{
        'allBookLists':searchbooklist,
        })

def allusers(request):
    if not request.user.is_authenticated():
        return mylogin(request)
        
    allusers = MyUser.objects.exclude(user=request.user)
    tuorist = MyUser.objects.get(user=request.user)
    
    return render(request,'booklist/allusers.html',{
        'allusers':allusers,
        'tuorist':tuorist,
        })

def addFriend(request):
    like = request.GET.get('like');
    someone = User.objects.get(username=like)
    
    likeuser = MyUser.objects.get(user=someone)
    myuser = MyUser.objects.get(user=request.user)
    myuser.addFriend(likeuser)
    myuser.save()

    return render(request,'booklist/success.html',{
        'title':"Add friend,Success!",
        })

def removeFriend(request):
    unlike = request.GET.get('like');
    someone = User.objects.get(username=unlike)

    unlikeUser = MyUser.objects.get(user=someone)

    myuser = MyUser.objects.get(user=request.user)
    myuser.removeFriend(unlikeUser)

    return render(request,'booklist/success.html',{
        'title':"Remove friend,Success!",
        })

def addPrivateFriend(request):
    like = request.GET.get('like');
    someone = User.objects.get(username=like)
    likeuser = MyUser.objects.get(user=someone)
    myuser = MyUser.objects.get(user=request.user)

    myuser.addPrivateFriend(likeuser)
    myuser.save()

    return render(request,'booklist/success.html',{
        'title':'AddPrivateFriend,Success!'
        })

def removePrivateFriend(request):
    like = request.GET.get('like');
    someone = User.objects.get(username=like)
    likeuser = MyUser.objects.get(user=someone)
    myuser = MyUser.objects.get(user=request.user)

    myuser.removePrivateFriend(likeuser)

    return render(request,'booklist/success.html',{
        'title':'RomovePrivateFriend,Success!'
        })

def alluserbooks(request):
    username = request.GET.get('username')

    user = User.objects.get(username=username)
    books= Book.objects.filter(user=user)
    booklists=BookList.objects.filter(user=user)

    myuser = MyUser.objects.get(user=user)
    isFriend = myuser.getFriend().filter(user=request.user)
    
    isPrivateFriend = myuser.getPrivateFriend().all()

    return render(request,'booklist/alluserbooks.html',{
        'user':user,
        'books':books,
        'booklists':booklists,
        'isFriend':isFriend,
        'isPrivateFriend':isPrivateFriend,
        })

# def isFriend(self,another):
#     friendship = FriendShip.objects.get(one=self,another=another)
#     return friendship

# User.isFriend = isFriend


def friendbooklist(request):
    if not request.user.is_authenticated():
        return mylogin(request)
        
    myuser = MyUser.objects.get(user=request.user)
    # friends = myuser.getFriend()
    friends = myuser.privatef_set.all()
    # logger.debug(friends)

    booklists = BookList.objects.none()
    for friend in friends.all():
        booklist = BookList.objects.filter(user=friend.getUser())
        booklists = booklists | booklist

    # logger.debug(booklists)
    return render(request,'booklist/friendbooklist.html',{
        'booklists':booklists,

        })