from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^books/$', views.books,name='books'),
    url(r'^bookin/$', views.bookin,name='bookin'),
    url(r'^tourist_bookin/$', views.tourist_bookin,name='tourist_bookin'),
    url(r'^addbook/$',views.addBook,name='addbook'),
	url(r'^success/$',views.success,name='success'),
	url(r'^minus/$',views.minus,name='minus'),
	url(r'^mylogin/$',views.mylogin,name='mylogin'),
	url(r'^rmnote/$',views.rmnote,name='rmnote'),
	url(r'^addblog/$',views.addBlog,name='addblog'),
	url(r'^rmblog/$',views.rmBlog,name='rmBlog'),
	url(r'^zodiac/$',views.zodiac,name='zodiac'),
	url(r'^register/$',views.register,name='register'),
	url(r'^logout/$',views.logout_view,name='logout'),
	url(r'^allbooks/$',views.allBooks,name='allbooks'),
	url(r'^addbooklist/$',views.addbooklist,name='addbooklist'),
	url(r'^allbooklist/$',views.allbooklist,name='allbooklist'),
	url(r'^searchBooklist/$',views.searchBooklist,name='searchBooklist'),
	url(r'^allusers/$',views.allusers,name='allusers'),
	url(r'^alluserbooks/$',views.alluserbooks,name='alluserbooks'),
	url(r'^other/$',views.other,name='other'),
	url(r'^addFriend/$',views.addFriend,name='addFriend'),
	url(r'^removeFriend/$',views.removeFriend,name='removeFriend'),
	url(r'^friendbooklist/$',views.friendbooklist,name='friendbooklist'),
	url(r'^addPrivateFriend/$',views.addPrivateFriend,name='addPrivateFriend'),
	url(r'^removePrivateFriend/$',views.removePrivateFriend,name='removePrivateFriend'),
	


    url(r'^$', views.index,name="index"),
    url(r'^index/$', views.index,name="index"),
]
