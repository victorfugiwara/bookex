from rest_framework import serializers
from core.models import UserProfile, Author, Category, Book, Library, Wish

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name', 'email', 'picture')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'picture', 'author', 'category')


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ('profile', 'book')


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('profile', 'book')
