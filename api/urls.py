from rest_framework import routers
from django.conf.urls import url, include

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
    url(r'^api-auth/', include('rest_framework.urls'))
]