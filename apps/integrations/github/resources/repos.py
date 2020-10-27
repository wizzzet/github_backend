from integrations.github.resources.base import GitHubListResource, \
    GitHubObjectResource


class ReposListResource(GitHubListResource):
    """Ресурс данных репозиториев пользователя GitHub"""

    endpoint = 'users/{user_slug}/repos'
    search_endpoint = 'search/users'


class RepoResource(GitHubObjectResource):
    """Ресурс данных отдельного репозитория пользователя GitHub"""

    endpoint = 'repos/{user_slug}/{repo_slug}'
    object_id_param = 'user_slug'
