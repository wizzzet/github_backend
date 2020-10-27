from abc import ABC, abstractmethod

from django.conf import settings
from django.utils.http import urlencode
import requests

from rest_framework.exceptions import APIException


class SearchMixin:

    search_endpoint = None

    def __init__(self, *args, **kwargs):
        super(SearchMixin, self).__init__(*args, **kwargs)
        self.search_mode = False

    def search(self, query):
        self.query_params['q'] = query
        self.search_mode = bool(self.search_endpoint)
        return self


class PaginateMixin:

    def paginate(self, page, per_page):
        self.query_params['page'] = page
        self.query_params['per_page'] = per_page
        return self

    def paginate_by_since(self, since):
        self.query_params['since'] = since
        return self


class GitHubResource(ABC):
    """Базовый класс ресурса данных GitHub"""

    endpoint = None
    method = 'get'

    def __init__(self, *args, **params):
        self.params = params
        self.query_params = {}
        self.result = None

    @abstractmethod
    def get_endpoint(self):
        return self.endpoint

    def build_url(self, **kwargs):
        endpoint = self.get_endpoint()
        assert endpoint

        endpoint_url = f'{settings.GITHUB_API_URL}/{endpoint}'
        url = endpoint_url.format(**self.params)

        if self.query_params:
            query_params = urlencode(self.query_params)
            if query_params:
                url += '?' + query_params

        return url

    def get_headers(self):
        return {
            'Accept': 'application/vnd.github.v3+json'
        }

    def call(self):
        url = self.build_url()
        headers = self.get_headers()

        method = getattr(requests, self.method.lower())
        response = method(url, headers=headers)

        if response.status_code < 300:
            self.result = response.json()
            return self.transform_result(self.result)

        raise APIException(detail=response.json(), code=response.status_code)

    def transform_result(self, result):
        """
        Преобразует результат получения данных из GitHub в приемлемый вид
        """
        return result


class GitHubListResource(SearchMixin, PaginateMixin, GitHubResource):
    """Ресурс данных GitHub в виде списка"""

    def get_endpoint(self):
        assert self.endpoint

        if self.search_mode:
            return self.search_endpoint or self.endpoint

        return self.endpoint

    def transform_result(self, result):
        if self.search_mode:
            return result['items']

        return result

    def get_list(self):
        return self.call()


class GitHubObjectResource(GitHubResource):
    """Ресурс данных GitHub в виде отдельного объекта"""

    object_id_param = 'object_id'

    def get_endpoint(self):
        return self.endpoint

    def get_object(self):
        return self.call()
