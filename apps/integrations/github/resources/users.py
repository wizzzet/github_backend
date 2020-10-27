from integrations.github.resources.base import GitHubListResource, \
    GitHubObjectResource


class UsersListResource(GitHubListResource):
    """Ресурс данных пользователей GitHub"""

    endpoint = 'users'
    search_endpoint = 'search/users'


class UserResource(GitHubObjectResource):
    """Ресурс данных отдельного пользователя GitHub"""

    endpoint = 'users/{user_slug}'
    object_id_param = 'user_slug'
