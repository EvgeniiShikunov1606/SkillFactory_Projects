from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdViewSet, ResponseViewSet, UserResponsesListView


router = DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'responses', ResponseViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("my-responses/", UserResponsesListView.as_view(), name="user-responses"),
]
