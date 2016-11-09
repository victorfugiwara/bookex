from django.conf.urls import include, url

from rest_framework import routers

from rest_framework_jwt.views import obtain_jwt_token

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserProfileViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'libraries', views.LibraryViewSet)
router.register(r'wishes', views.WishViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login', obtain_jwt_token),
    url(r'^users/(?P<id_user>[0-9]+)/libraries$', views.UserLibrary.as_view()),
    url(r'^users/(?P<id_user>[0-9]+)/libraries/(?P<id_book>[0-9]+)$',
        views.UserLibraryDetail.as_view()),
    url(r'^users/(?P<id_user>[0-9]+)/wishes$', views.UserWish.as_view()),
    url(r'^users/(?P<id_user>[0-9]+)/wishes/(?P<id_book>[0-9]+)$',
        views.UserWishDetail.as_view()),
    url(r'^categories/(?P<id_category>[0-9]+)/books$',
        views.BooksCategory.as_view()),
    url(r'^authors/(?P<id_author>[0-9]+)/books$', views.BooksAuthor.as_view()),
    url(r'^users/(?P<id_user>[0-9]+)/combinations$',
        views.Combinations.as_view()),
]
