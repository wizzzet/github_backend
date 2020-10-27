from django.conf import settings
from django.template import defaultfilters as filters
from django.template.defaultfilters import urlencode

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from snippets.choices import StatusChoices


__all__ = (
    'FileField', 'ImageField', 'PublishedRelationField', 'PretextField',
    'SlugRelatedToPkField', 'SVGField'
)


class FileField(serializers.FileField):
    def to_representation(self, value):
        result = super(FileField, self).to_representation(value)
        if result:
            return '%s%s' % (settings.MEDIA_URL, urlencode(result))


class ImageField(serializers.ImageField):
    def to_representation(self, value):
        result = super(ImageField, self).to_representation(value)
        if result:
            return '%s%s' % (settings.MEDIA_URL, urlencode(result))


class PretextField(serializers.ReadOnlyField):
    def to_representation(self, value):
        result = super(PretextField, self).to_representation(value)
        if result:
            return filters.linebreaksbr(result)


class PublishedRelationField(serializers.Field):
    """"""
    def __init__(self, serializer_class, many=True, limit=None, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        self.serializer_class = serializer_class
        self.many = many
        self.limit = limit
        super(PublishedRelationField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        qs = None
        if self.many:
            qs = getattr(value, self.field_name).published()
            if self.limit is not None:
                qs = qs[:self.limit]
        else:
            obj = getattr(value, self.field_name)
            if obj and obj.status == StatusChoices.PUBLIC.value:
                qs = obj

        if qs:
            return self.serializer_class(qs, many=self.many).data

        return [] if self.many else None


class SlugRelatedToPkField(SlugRelatedField):
    def to_internal_value(self, data):
        obj = super(SlugRelatedToPkField, self).to_internal_value(data)
        return obj.pk


class SVGField(serializers.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs['source'] = '*'
        self.image_field = list(args).pop(0)
        args = tuple(args[1:])
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        file = getattr(value, self.image_field)
        if file:
            with file.open(mode='r'):
                lines = file.readlines()
            return ''.join(lines)
