"""Defines the endpoints of the api."""
from core.models import Author, Book, Category, Library, UserProfile, Wish

from django.http import Http404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AuthorSerializer,
    BookSerializer,
    CategorySerializer,
    CombinationSerializer,
    LibrarySerializer,
    UserProfileSerializer,
    WishSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """Define the User profile endpoints."""

    queryset = UserProfile.objects.all().order_by('name')
    serializer_class = UserProfileSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """Define the Authors endpoints."""

    queryset = Author.objects.all().order_by('last_name')
    serializer_class = AuthorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Define the Categories endpoints."""

    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    """Define the Books endpoints."""

    queryset = Book.objects.all().order_by('name')
    serializer_class = BookSerializer


class LibraryViewSet(viewsets.ModelViewSet):
    """Define the Library of the user endpoints."""

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class WishViewSet(viewsets.ModelViewSet):
    """Define the wishe endpoints."""

    queryset = Wish.objects.all()
    serializer_class = WishSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """Override the return of the login endpoint."""
    profile = UserProfile.objects.get(user=user)
    return {
        'token': token,
        'profile': UserProfileSerializer(
            profile,
            context={'request': request}
        ).data
    }


class UserLibrary(APIView):
    """Books that the user has endpoint."""

    def get(self, request, id_user, format=None):
        """Return the books of the user of the parameter."""
        libraries = Library.objects.filter(profile_id=id_user)
        serializer = LibrarySerializer(libraries, many=True)
        return Response(serializer.data)

    def post(self, request, id_user, format=None):
        """Include a book on the library of the user."""
        library = Library(profile_id=id_user, book_id=request.data['book_id'])
        library.save()
        serializer = LibrarySerializer(library)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLibraryDetail(APIView):
    """Library endpoints."""

    def delete(self, request, id_user, id_book, format=None):
        """Remove the book from the library of the user."""
        try:
            library = Library.objects.filter(
                profile_id=id_user,
                book_id=id_book
            )
            library.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Library.DoesNotExist:
            raise Http404


class UserWish(APIView):
    """Books that the user wants endpoints."""

    def get(self, request, id_user, format=None):
        """Return the list of books that the user wants."""
        wishes = Wish.objects.filter(profile_id=id_user)
        serializer = WishSerializer(wishes, many=True)
        return Response(serializer.data)

    def post(self, request, id_user, format=None):
        """Insert a book on the list of wishes of the user."""
        wish = Wish(profile_id=id_user, book_id=request.data['book_id'])
        wish.save()
        serializer = WishSerializer(wish)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserWishDetail(APIView):
    """Wishes endpoint."""

    def delete(self, request, id_user, id_book, format=None):
        """Remove the book from the wishes of the user."""
        try:
            wish = Wish.objects.filter(profile_id=id_user, book_id=id_book)
            wish.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Wish.DoesNotExist:
            raise Http404


class BooksCategory(APIView):
    """Books of the category endpoint."""

    def get(self, request, id_category, format=None):
        """Return the list of books that are from the category."""
        books = Book.objects.filter(category_id=id_category)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BooksAuthor(APIView):
    """Books of the author enpoint."""

    def get(self, request, id_author, format=None):
        """Return the list of books that are from the author."""
        books = Book.objects.filter(author_id=id_author)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class Combinations(APIView):
    """Combinations of exchanges endpoint."""

    def get(self, request, id_user, format=None):
        """Return the list of possible combinations of exchanges."""
        id_book_library = None
        id_book_wish = None
        # parameters to filter the book from his library that he'll change
        # and the one that he wants
        if 'id_book_library' in request.query_params:
            id_book_library = request.query_params['id_book_library']
        if 'id_book_wish' in request.query_params:
            id_book_wish = request.query_params['id_book_wish']

        # get user library
        user_libraries = Library.objects.filter(profile_id=id_user)
        if id_book_library:
            # apply filter of the book, if isn't empty
            user_libraries = user_libraries.filter(book_id=id_book_library)

        user_wishes = Wish.objects.filter(profile_id=id_user)
        if id_book_wish:
            # apply filter of the book, if isn't empty
            user_wishes = user_wishes.filter(book_id=id_book_wish)

        combinations = []
        for lib in user_libraries:
            # for each book from user's library, find possible exchanges

            # find look for people who wants the user's book
            others_wishes = Wish.objects.exclude(profile_id=id_user).filter(
                book_id=lib.book_id)

            for others_wish in others_wishes:
                # for each other users wishes, search for a book that the
                # user wants
                others_libraries = Library.objects.filter(
                    profile_id=others_wish.profile_id)

                for others_lib in others_libraries:
                    # search the book of the other users library on the
                    # user wishes
                    if user_wishes.filter(book_id=others_lib.book_id).exists():
                        # user that have the book, his name, book that the
                        # user wants, book of user's library that he'll change
                        c = {
                            'profile': others_lib.profile,
                            'book_wish': others_lib.book,
                            'book_library': lib.book
                        }

                        combinations.append(c)

        return Response(CombinationSerializer(combinations, many=True).data)
