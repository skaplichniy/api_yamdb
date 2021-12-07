from django.urls import path, include
from rest_framework import routers
from .views import ReviewViewSet, CommentsViewSet, CategoryViewSet, GenreViewSet, TitlesViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, signup, get_token, me

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('users',
                   UserViewSet,
                   basename='users')
router_v1.register(r'reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'reviews/(?P<rewiev_id>[^/.]+)/comments',
    CommentsViewSet,
    basename='comment'
)
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/users/me/', me, name='me'),
        ]





#router_v1 = DefaultRouter
#router_v1.register('users',
 #                  UserViewSet,
  #                 basename='users')

#urlpatterns = [
 #   path('v1/auth/signup/', signup, name='signup'),
  #  path('v1/auth/token/', get_token, name='get_token'),
  #  path('v1/', include(router_v1.urls)),
#]
