from photologue.models import Photo, Gallery
from rest_framework import serializers


class PhotoViewSerializer(serializers.ModelSerializer):
    gallery = serializers.CharField(required=False)

    class Meta:
        model = Photo
        fields = ['id', 'title', 'slug', 'gallery', 'date_added', 'is_public', 'image']

    def to_representation(self, instance):
        represented = super().to_representation(instance)
        request = self.context.get('request')
        represented['slug'] = request.build_absolute_uri(f"/photologue/photo/{represented['slug']}/")
        return represented

class GalleryListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'title', 'slug', ]

    def to_representation(self, instance):
        represented = super().to_representation(instance)
        request = self.context.get('request')
        represented['slug'] = request.build_absolute_uri(f"/photologue/gallery/{represented['slug']}/")
        represented['detail'] = request.build_absolute_uri(represented['id'])
        return represented

class GalleryViewSerializer(serializers.ModelSerializer):
    photos = PhotoViewSerializer(many=True)
    class Meta:
        model = Gallery
        fields = ['id', 'title', 'slug', 'photos', ]

    def to_representation(self, instance):
        represented = super().to_representation(instance)
        request = self.context.get('request')
        represented['slug'] = request.build_absolute_uri(f"/photologue/gallery/{represented['slug']}/")
        return represented
