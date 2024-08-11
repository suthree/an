from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TestView

router = DefaultRouter()
router.register(r"test", TestView, basename="test")

urlpatterns = [
    path("", include(router.urls)),
    # path("test/", TestView, name="test"),
]
