from django.conf import settings
from django.db import models

from datetime import date
from django.contrib.auth.models import User


from django.utils.log import logging
logger = logging.getLogger('django.request')

# Create your models here.

class Question(models.Model):
	question_text = models.CharField(max_length=200)

class BookManager(models.Manager):
	def create_book(self,name,author,publish,date,isbn,user,summary):
		book = Book.create(name = name,author=author,publish=publish,date=date,isbn=isbn,user=user,summary=summary)
		return book

class Book(models.Model):
	name = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	publish = models.CharField(max_length=200)
	date = models.DateField()
	ISBN13 = models.CharField(default='',max_length=200)
	user = models.ForeignKey(User,null=True,related_name='user_set')
	summary = models.TextField(default='')

	amazonURL = models.URLField(default='',max_length=200,null=True)

	objects = BookManager()
	
	@classmethod
	def create(cls,name,author,publish,date,isbn,user,summary):
		book = cls(name=name,author=author,publish=publish,date=date,ISBN13=isbn,user=user,summary=summary)
		return book

	def setUser(self,user):
		self.user = user

	def getamazonURL(self):
		self.amazonURL = "https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords="
		
		if len(self.ISBN13)<=1:
			url = self.amazonURL + self.name
		else:
			url = self.amazonURL + self.ISBN13
		return url

	def __unicode__(self):
		return '%s' % (self.name)

class NoteManager(models.Manager):
	def create_note(self,time,text,book):
		note= Note.create(time=time,text=text,book=book)
		return note

class Note(models.Model):
	time = models.DateTimeField(null=True,max_length=100)
	text = models.TextField()
	book = models.ForeignKey(Book,related_name='notes')

	objects = NoteManager()

	@classmethod
	def create(cls,time,text,book):
		note = cls(time=time,text=text,book=book)
		return note

	def setBook(self,book):
		self.book=book

	def __unicode__(self):
		return '%s' % (self.text)
		
class Blog(models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField()
	user = models.ForeignKey(User,null=True,related_name='blog_set')

	def setUser(self,user):
		self.user=user

	@classmethod
	def create(cls,title,text):
		blog = cls(title=title,text=text)
		return blog

	def __unicode__(self):
		return '%s' % (self.title)

class BookList(models.Model):
	title = models.CharField(null=True,default='',max_length=100)
	introduce = models.CharField(max_length=400)
	books = models.ManyToManyField(Book)
	user = models.ForeignKey(User,null=True,related_name='booklist_set')

	def addBook(self,book):
		self.books.add(book)

	def getBook(self):
		return self.books

	def __unicode__(self):
		return '%s' % (self.introduce)

class MyUser(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='me_set')
	friend = models.ManyToManyField('self',blank=True,related_name='f_set')

	privatefriend = models.ManyToManyField('self',
		blank=True,
		through='FriendShip',through_fields=('friend','me'),symmetrical=False,
		related_name='privatef_set',)

	@classmethod
	def create(cls,user):
		myuser = cls(user=user)
		return myuser

	def addFriend(self,somebody):
		if self.user.get_username()==somebody.user.get_username():
			return
		self.friend.add(somebody)
		self.save()

	def removeFriend(self,somebody):
		self.friend.remove(somebody)
		self.save()

	def getFriend(self):
		return self.friend

	def addPrivateFriend(self,somebody):		
		pf = FriendShip.objects.create(friend=somebody,me=self)
		pf.save()

		# self.privatefriend.all()
		# logger.debug(self.privatef_set.all())

	def removePrivateFriend(self,somebody):
		# logger.debug('removePrivateFriend..start')
		FriendShip.objects.get(friend=somebody).delete()


	def getPrivateFriend(self):
		return self.privatefriend
		# pass

	def getUser(self):
		return self.user

	def getName(self):
		return self.user.get_username()


	def __unicode__(self):
		return '%s' % self.user

class FriendShip(models.Model):
	friend = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name="friendship_other",)
	me = models.ForeignKey(MyUser,on_delete=models.CASCADE)

	@classmethod
	def create(cls,friend,me):
		fs = cls(friend=friend,me=me)
		return fs

	def __unicode__(self):
		return '%s + %s' % (self.friend,self.me)


# class Ship(models.Model):
# 	name = models.CharField(default='',max_length=50)
	
	
# 	def __unicode__(self):
# 		return '%s' % self.name

# class Group(models.Model):
# 	name = models.CharField(max_length=128)
# 	members = models.ManyToManyField(Ship,through='MemberShip',through_fields=('group','ship'),)

# 	child = models.ManyToManyField('self',through='Tree',through_fields=('group','child'),symmetrical=False,)
# 	def __unicode__(self):
# 		return '%s' % self.name

# class MemberShip(models.Model):
# 	group=models.ForeignKey(Group,on_delete=models.CASCADE)
# 	ship = models.ForeignKey(Ship,on_delete=models.CASCADE)

# 	inviter = models.ForeignKey(Ship,on_delete=models.CASCADE,related_name="membership_invites",)

# 	invite_reason= models.CharField(max_length=64)

# 	def __unicode__(self):
# 		return '%s' % (self.invite_reason)

# class Tree(models.Model):
# 	group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name="tree_group",)
# 	child=models.ForeignKey(Group,on_delete=models.CASCADE)

# 	def __unicode__(self):
# 		return '%s' % (self.group)
