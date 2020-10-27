from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from snippets.api.swagger.schema import SimpleAutoSchema


class PublicViewMixin(object):
    permission_classes = (AllowAny,)


class BaseAPIViewMixin(object):
    swagger_schema = SimpleAutoSchema


class PublicAPIViewMixin(PublicViewMixin, BaseAPIViewMixin):
    pass


class BaseListAPIView(ListAPIView):
    pass


class BaseRetrieveAPIView(RetrieveAPIView):
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class PageRetrieveAPIView(RetrieveAPIView):
    """Позволяет получать объекты "страниц" """

    def get_object(self):
        return self.queryset.model.get_solo()
