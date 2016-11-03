from rest_framework import viewsets
from .serializers import UserProfileSerializer, AuthorSerializer, CategorySerializer, BookSerializer, LibrarySerializer, WishSerializer, CombinationSerializer
from core.models import UserProfile, Author, Category, Book, Library, Wish

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('name')
    serializer_class = UserProfileSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class WishViewSet(viewsets.ModelViewSet):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    profile = UserProfile.objects.get(user=user)
    return {
        'token': token,
        'profile': UserProfileSerializer(profile, context={'request': request}).data
    }


class UserLibrary(APIView):

    def get(self, request, id_user, format=None):
        libraries = Library.objects.filter(profile_id=id_user)
        serializer = LibrarySerializer(libraries, many=True)
        return Response(serializer.data)

    def post(self, request, id_user, format=None):
        library = Library(profile_id=id_user, book_id=request.data['book_id'])
        library.save()
        serializer = LibrarySerializer(library)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLibraryDetail(APIView):

    def delete(self, request, id_user, id_book, format=None):
        try:
            library = Library.objects.filter(profile_id=id_user, book_id=id_book)
            library.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Library.DoesNotExist:
            raise Http404
        


class UserWish(APIView):

    def get(self, request, id_user, format=None):
        wishes = Wish.objects.filter(profile_id=id_user)
        serializer = WishSerializer(wishes, many=True)
        return Response(serializer.data)

    def post(self, request, id_user, format=None):
        wish = Wish(profile_id=id_user, book_id=request.data['book_id'])
        wish.save()
        serializer = WishSerializer(wish)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserWishDetail(APIView):

    def delete(self, request, id_user, id_book, format=None):
        try:
            wish = Wish.objects.filter(profile_id=id_user, book_id=id_book)
            wish.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Wish.DoesNotExist:
            raise Http404
        

class BooksCategory(APIView):

    def get(self, request, id_category, format=None):
        books = Book.objects.filter(category_id=id_category)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BooksAuthor(APIView):

    def get(self, request, id_author, format=None):
        books = Book.objects.filter(author_id=id_author)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class Combination():
    id_user = None
    name = None
    book_wish = None
    book_library = None

    def __str__(self):
        return str(self.id_user) + ' - ' + self.name + ' - ' + str(self.book_wish) + ' - ' + str(self.book_library)

class Combinations(APIView):

    def get(self, request, id_user, format=None):
        combinations = []

        id_book_library = None
        id_book_wish = None
        # parameters to filter the book from his library that he'll change and the one that he wants
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


        for lib in user_libraries:
            # for each book from user's library, find possible exchanges

            # find look for people who wants the user's book
            others_wishes = Wish.objects.exclude(profile_id=id_user).filter(book_id=lib.book_id)

            for others_wish in others_wishes:
                # for each other users wishes, search for a book that the user wants
                others_libraries = Library.objects.filter(profile_id=others_wish.profile_id)

                for others_lib in others_libraries:
                    # search the book of the other users library on the user wishes
                    if user_wishes.filter(book_id=others_lib.book_id).exists():
                        # user that have the book, his name, book that the user wants, book of user's library that he'll change
                        c = {
                            'profile' : others_lib.profile,
                            'book_wish' : others_lib.book,
                            'book_library' : lib.book
                            }
                        #c.profile = UserProfileSerializer(others_lib.profile)
                        #c.book_wish = BookSerializer(others_lib.book)
                        #c.book_library = BookSerializer(lib.book)

                        combinations.append(c)

        print(combinations)

        return Response(CombinationSerializer(combinations, many=True).data)
