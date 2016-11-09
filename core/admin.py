from django.contrib import admin

from .models import Author, Book, Category, Library, UserProfile, Wish


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'image_tag', )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'image_tag', )


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('profile', 'book')


class WishAdmin(admin.ModelAdmin):
    list_display = ('profile', 'book')


admin.site.register(Book, BookAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Wish, WishAdmin)

admin.site.register(Author)
admin.site.register(Category)
