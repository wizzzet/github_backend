from django.urls import path

from github.api import views


app_name = 'github'


urlpatterns = (
    path(
        'users/',
        views.UsersListView.as_view(),
        name='users'
    ),
    path(
        'users/<slug:user_slug>/',
        views.UserView.as_view(),
        name='user'
    ),
    path(
        'users/<slug:user_slug>/followers/',
        views.UserFollowersView.as_view(),
        name='user_followers'
    ),
    path(
        'users/<slug:user_slug>/repos/',
        views.UserReposListView.as_view(),
        name='user_repos'
    ),
    path(
        'users/<slug:user_slug>/repos/<slug:repo_slug>/',
        views.UserRepoView.as_view(),
        name='user_repo'
    )
)
