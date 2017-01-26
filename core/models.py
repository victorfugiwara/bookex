"""Models of the project."""
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """User data."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    picture = models.ImageField(
        upload_to='profile_pictures/',
        default='no-image.png')

    def __str__(self):
        """Return the name of the user."""
        return self.user.first_name + ' ' + self.user.last_name

    def image_tag(self):
        """Return the <img> tag filled with the full path of the picture."""
        # return '<img src="/media/%s" />' % self.picture
        return '<img style="max-height: 100px;" src="/media/{}" />'.format(
            self.picture)
    image_tag.short_description = 'Picture'
    image_tag.allow_tags = True


class Category(models.Model):
    """Categories of the books."""

    name = models.CharField(max_length=200)

    def __str__(self):
        """Return the name of the category."""
        return self.name


class Author(models.Model):
    """Author of the books."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        """Return the first and the last name of the author."""
        return self.first_name + ' ' + self.last_name


class Book(models.Model):
    """Books availabled."""

    name = models.CharField(max_length=200)
    picture = models.ImageField(
        upload_to='book_pictures/',
        default='no-image.png')
    author = models.ForeignKey(Author)
    category = models.ForeignKey(Category)

    def __str__(self):
        """Return an identification of the book.

        The name of the book is followed by the last name and the first
        name of the author.
        """
        return self.name
        ' ('
        self.author.last_name + ', '
        self.author.first_name
        ')'

    def image_tag(self):
        """Return the <img> tag filled with the full path of the picture."""
        # return '<img src="/media/%s" />' % self.picture
        return '<img style="max-height: 100px;" src="/media/{}" />'.format(
            self.picture)
    image_tag.short_description = 'Picture'
    image_tag.allow_tags = True


class Library(models.Model):
    """Books that the user has."""

    profile = models.ForeignKey(UserProfile)
    book = models.ForeignKey(Book)

    def __str__(self):
        """Return the name of the book."""
        return self.book.name


class Wish(models.Model):
    """Books that the user wishes."""

    profile = models.ForeignKey(UserProfile)
    book = models.ForeignKey(Book)

    def __str__(self):
        """Return the name of the book."""
        return self.book.name
