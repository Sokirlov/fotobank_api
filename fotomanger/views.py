import copy
import os

from django.utils.decorators import method_decorator
from slugify import slugify
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.files.base import ContentFile
from django.utils.timezone import now
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from photologue.models import Photo, Gallery

from fotomanger.filters import PhotoFilter
from fotomanger.serializers import PhotoViewSerializer, GalleryViewSerializer, GalleryListViewSerializer

@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Show all photo with pagination by default 20 items "
                          "(correct pagination in project settings)\n"
                          "You can use filtration by [Date taken, Title, Slug]",
    manual_parameters =[
        openapi.Parameter('date_taken__gte', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date-time',
                          description="Returns all elements with "
                                      "a date greater than the selected value. "
                                      "\nUse the format YYYY-MM-DD for the request."),
        openapi.Parameter('date_taken__lte', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date-time',
                          description="Returns all elements with "
                                      "a date less than the selected value. "
                                      "\nUse the format YYYY-MM-DD for the request."),
        openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                          description="partial match, case insensitive"),
        openapi.Parameter('slug', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                          description="partial match, case insensitive")
    ],
    responses={200: PhotoViewSerializer(many=True)}
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Upload photo. \n"
                          "Required parameters to valid upload photo [ title, slug, gallery image]\n"
                          "Title and slug must be uniq\n"
                          "If `is_public` is set to `True`, the photographs will appear in the default views. "
                          "If set to `False`, they will only be visible in the admin panel and via the API.",
    request_body=PhotoViewSerializer,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Detail by photo",))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_description="Update photo data"))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_description="Delete photo"))
class PhotoView(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    serializer_class = PhotoViewSerializer
    http_method_names = ['get', 'post', 'put',  'delete']
    filterset_class = PhotoFilter

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

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Return list all gallery",
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Return all photo by this gallery",
))

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
