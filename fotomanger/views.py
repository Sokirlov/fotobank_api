import copy
import os

from rest_framework.parsers import MultiPartParser, FormParser
from slugify import slugify
from django.core.files.base import ContentFile
from django.utils.timezone import now
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from photologue.models import Photo, Gallery
from fotomanger.serializers import PhotoViewSerializer, GalleryViewSerializer, GalleryListViewSerializer


class PhotoView(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    serializer_class = PhotoViewSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filterset_fields = ['date_taken', 'title', 'slug']

    @staticmethod
    def custom_upload_to(filename):
        """
        Create custom path for upload file.
        Like: media/custom_photos/<Year>/<Month>/<Day>/<filename>.
        """
        return os.path.join(now().strftime('%Y/%m/%d'), filename)

    @staticmethod
    def get_slug(txt):
        return slugify(txt, max_length=250, word_boundary=True)

    def add_gallery(self, photo, gallery_: str):
        slug_ = self.get_slug(gallery_)
        gallery, _ = Gallery.objects.get_or_create(title=gallery_, slug=slug_)
        gallery.photos.add(photo)

    def create(self, request, *args, **kwargs):
        data_ = copy.deepcopy(request.data)
        uploaded_file = request.FILES.get('image')
        if not uploaded_file:
            return Response({"detail": "Image file is required."}, status=status.HTTP_400_BAD_REQUEST)
        new_path = self.custom_upload_to(uploaded_file.name)
        new_file = ContentFile(uploaded_file.read(), name=new_path)
        data_['image'] = new_file

        gallery = data_.pop('gallery')
        if isinstance(gallery, list):
            gallery = gallery[0]

        serializer = self.get_serializer(data=data_)
        serializer.is_valid(raise_exception=True)
        photo = serializer.save()
        try:
            self.add_gallery(photo, gallery)
        except Exception as e:
            print("Exception as ", e)
            return Response(e, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = GalleryListViewSerializer
    http_method_names = ['get', ]

    def get_serializer_class(self):
        if self.action == 'list':
            return GalleryListViewSerializer
        else:
            return GalleryViewSerializer
