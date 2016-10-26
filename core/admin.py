from django.contrib import admin

from .models import UserProfile, Author, Category, Book, Library, Wish

class BookAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'author', 'category', 'image_tag', )

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'email', 'image_tag', )


admin.site.register(Book, BookAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Library)
admin.site.register(Wish)
