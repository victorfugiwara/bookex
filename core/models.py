from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    picture = models.ImageField(upload_to = 'profile_pictures/', default = 'profile_pictures/None/no-image.png')

    def __str__(self):
        return self.name

    def image_tag(self):
        return u'<img src="/media/%s" />' % self.picture
    image_tag.short_description = 'Picture'
    image_tag.allow_tags = True

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Book(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to = 'book_pictures/', default = 'book_pictures/None/no-image.png')
    author = models.ForeignKey(Author)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name + ' (' + self.author.last_name + ', ' + self.author.first_name + ')'

    def image_tag(self):
        return u'<img src="/media/%s" />' % self.picture
    image_tag.short_description = 'Picture'
    image_tag.allow_tags = True

class Library(models.Model):
    profile = models.ForeignKey(UserProfile)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.book.name

class Wish(models.Model):
    profile = models.ForeignKey(UserProfile)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.book.name
