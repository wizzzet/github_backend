from github.api import serializers
from integrations.github import resources
from integrations.github.views import GitHubListAPIView, \
    GitHubRetrieveAPIView, GitHubParentViewMixin


class UsersListView(GitHubListAPIView):
    """
    Представление списка пользователей GitHub.
    Поддверживает поиск через параметр `query` и пагинацию
    """

    resource_class = resources.UsersListResource
    serializer_class = serializers.UserSerializer


class UserView(GitHubRetrieveAPIView):
    """Представление пользователя GitHub"""

    param_name = 'user_slug'
    kwarg_name = 'user_slug'
    resource_class = resources.UserResource
    serializer_class = serializers.UserDetailSerializer


class UserRelatedViewMixin(GitHubParentViewMixin):
    """Миксин представлений зависимых объектов пользователя GitHub"""

    parent_param_name = 'user_slug'
    parent_kwarg_name = 'user_slug'


class UserFollowersView(UserRelatedViewMixin, GitHubListAPIView):
    """
    Представление списка подписчиков пользователя GitHub.
    Поддверживает поиск через параметр `query` и пагинацию
    """

    resource_class = resources.FollowersListResource
    serializer_class = serializers.UserSerializer


class UserReposListView(UserRelatedViewMixin, GitHubListAPIView):
    """
    Представление списка репозиториев пользователя GitHub.
    Поддверживает поиск через параметр `query` и пагинацию
    """
    resource_class = resources.ReposListResource
    serializer_class = serializers.RepoSerializer


class UserRepoView(UserRelatedViewMixin, GitHubRetrieveAPIView):
    """Представление репозитория пользователя GitHub"""

    param_name = 'repo_slug'
    kwarg_name = 'repo_slug'
    resource_class = resources.RepoResource
    serializer_class = serializers.RepoDetailSerializer
