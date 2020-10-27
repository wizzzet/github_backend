from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView


class GitHubAPIView(APIView):
    """Базовый класс для представлений данных из GitHub"""

    resource_class = None
    endpoint_resource_name = None
    serializer_class = None

    def get_resource_class(self):
        assert self.resource_class is not None, (
                '"%s" should either include a `resource_class` attribute, '
                'or override the `get_resource_class()` method.'
                % self.__class__.__name__
        )

        return self.resource_class

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
                '"%s" should either include a `serializer_class` attribute, '
                'or override the `get_serializer_class()` method.'
                % self.__class__.__name__
        )

        return self.serializer_class

    def get_resource(self):
        resource_class = self.get_resource_class()
        kwargs = self.get_resource_kwargs()
        return resource_class(**kwargs)

    def get_resource_kwargs(self):
        return {}


class GitHubParentViewMixin(object):
    """Миксин представления, инициирующий зависимые представления"""

    parent_param_name = 'parent_id'
    parent_kwarg_name = 'parent_id'

    def get_resource_kwargs(self):
        kwargs = super(GitHubParentViewMixin, self).get_resource_kwargs()
        kwargs[self.parent_param_name] = self.kwargs.get(
            self.parent_kwarg_name
        )
        return kwargs


class GitHubListAPIView(GitHubAPIView):
    """Представление данных из GitHub в виде списка"""

    default_per_page = 20
    max_per_page = 100

    def get_page(self):
        page = self.request.query_params.get('page')
        if page is None:
            return 1

        try:
            page = int(page)
        except (ValueError, TypeError):
            raise ParseError({
                'page': _('Некорректный номер страницы')
            })

        if page < 1:
            raise ValidationError({
                'page': _('Номер страницы меньше 1')
            })

        return page

    def get_per_page(self):
        per_page = self.request.query_params.get('per_page')
        if per_page is None:
            return self.default_per_page

        try:
            per_page = int(per_page)
        except (ValueError, TypeError):
            raise ParseError({
                'per_page': _(
                    'Некорректный параметр количества элементов на странице'
                )
            })

        if per_page < 1:
            raise ValidationError({
                'per_page': _('Количество элементов на странице меньше 1')
            })

        if per_page > self.max_per_page:
            raise ValidationError({
                'per_page': _(
                    'Количество элементов на странице больше максимального '
                    '(%s)' % self.max_per_page
                )
            })

        return per_page

    def get_since(self):
        since = self.request.query_params.get('since')
        if since is None:
            return None

        try:
            since = int(since)
        except (ValueError, TypeError):
            raise ParseError({
                'since': _('Некорректный параметр since')
            })

        if since < 1:
            raise ValidationError({
                'per_page': _('параметр since меньше 1')
            })

        return since

    def get(self, request, *args, **kwargs):
        resource = self.get_resource()

        query = self.request.query_params.get('query')
        if query:
            resource = resource.search(query)

        page = self.get_page()
        per_page = self.get_per_page()

        since = self.get_since()
        if since is not None:
            resource = resource.paginate_by_since(since)

        elif page and per_page:
            resource = resource.paginate(page, per_page)

        serializer = self.get_serializer_class()
        result = resource.get_list()
        return Response(serializer(result, many=True).data)


class GitHubRetrieveAPIView(GitHubAPIView):
    """Представление данных из GitHub в виде отдельного объекта"""

    param_name = 'parent_id'
    kwarg_name = 'parent_id'

    def get_resource_kwargs(self):
        kwargs = super(GitHubRetrieveAPIView, self).get_resource_kwargs()
        kwargs[self.param_name] = self.kwargs.get(self.kwarg_name)
        return kwargs

    def get(self, request, *args, **kwargs):
        resource = self.get_resource()
        obj = resource.get_object()
        serializer = self.get_serializer_class()
        return Response(serializer(obj).data)
