from django.urls import include, path
from rest_framework import routers

from tutorial.quickstart import views

from fotomanger.views import PhotoView, GalleryViewSet

router = routers.DefaultRouter()
router.register(r'photo', PhotoView)
router.register(r'gallery', GalleryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]