from integrations.github.resources.base import GitHubListResource


class FollowersListResource(GitHubListResource):
    """Ресурс данных подписчиков пользователя GitHub"""

    endpoint = 'users/{user_slug}/followers'
