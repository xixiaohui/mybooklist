from django import forms

import datetime

from models import Book
from django.utils.log import logging
logger = logging.getLogger('django.request')

class BookForm(forms.Form):
	name = forms.CharField(label='Book Name',max_length=100)
	author = forms.CharField(label='Author Name',initial='?',max_length=100)
	publish = forms.CharField(label='Publisher',initial='?',max_length=100)
	date = forms.DateField(label='Date',initial= datetime.datetime.now())
	ISBN13= forms.CharField(label='ISBN13',initial='?',max_length=100)
	summary = forms.CharField(label='summary',initial='',widget=forms.Textarea)

class LogInForm(forms.Form):
	name = forms.CharField(label='username',max_length=100)
	word = forms.CharField(label='password',max_length=100)

class RegisterForm(forms.Form):
	username = forms.CharField(label='username',max_length=100)
	password = forms.CharField(label='password',max_length=100)
	email = forms.EmailField(label="email",max_length=100)

	# def clean(self):
	# 	return self.cleaned_data

class NoteForm(forms.Form):
	# time = forms.DateTimeField(label='',initial='2006-10-25 14:30:59',)
	text = forms.CharField(label='',initial='',widget=forms.Textarea)


class BlogForm(forms.Form):
	title = forms.CharField(label='',initial="title",max_length=100)
	text = forms.CharField(label='',initial='',widget=forms.Textarea)


class BirthdayForm(forms.Form):
	year = forms.CharField(label='year',initial="2016",max_length=100)
	month = forms.CharField(label='month',initial="5",max_length=100)
	day = forms.CharField(label='day',initial="5",max_length=100)

class ZodiacForm(forms.Form):
	date = forms.DateField(label="date",initial=datetime.datetime.now())

class BookListForm(forms.Form):
	title = forms.CharField(label='title',max_length=100)
	introduce = forms.CharField(label='introduce',initial='',widget=forms.Textarea)
	books = forms.ModelMultipleChoiceField(queryset=None)

	def setBooksQueryset(self,myqueryset):
		self.fields['books'].queryset = myqueryset