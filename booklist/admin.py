from django.contrib import admin
from .models import Book,Note,Blog,BookList,MyUser,FriendShip



class BookAdmin(admin.ModelAdmin):
    list_display = ('name','author','publish','date','user','ISBN13','amazonURL')
   
class NoteAdmin(admin.ModelAdmin):
	list_display = ('text','book')

class BlogAdmin(admin.ModelAdmin):
	list_display = ('title','user') 

class BookListAdmin(admin.ModelAdmin):
	list_display = ('title','user',)

class MyUserAdmin(admin.ModelAdmin):
	list_display=('user',)

class ShipAdmin(admin.ModelAdmin):
	list_display=('name',)

class GroupAdmin(admin.ModelAdmin):
	list_display=('name',)	

class MemberShipAdmin(admin.ModelAdmin):
	list_display=('group','ship','inviter','invite_reason',)

class FriendShipAdmin(admin.ModelAdmin):
	list_display=('me','friend',)


admin.site.register(Book,BookAdmin)
admin.site.register(Note,NoteAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(BookList,BookListAdmin)
admin.site.register(MyUser,MyUserAdmin)
# admin.site.register(Ship,ShipAdmin)
# admin.site.register(Group,ShipAdmin)
# admin.site.register(MemberShip,MemberShipAdmin)
admin.site.register(FriendShip,FriendShipAdmin)
