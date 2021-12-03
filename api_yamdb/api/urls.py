from django.urls import path, include
from rest_framework import routers
from .views import ReviewViewSet, CommentsViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'reviews', ReviewViewSet)
router.register(
    r'reviews/(?P<rewiev_id>[^/.]+)/comments',
    CommentsViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]