from rest_framework import serializers


class RepoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    node_id = serializers.CharField()
    name = serializers.CharField()
    full_name = serializers.CharField()
    private = serializers.BooleanField()
    html_url = serializers.CharField()
    description = serializers.CharField()
    fork = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    pushed_at = serializers.DateTimeField()
    git_url = serializers.CharField()
    ssh_url = serializers.CharField()
    clone_url = serializers.CharField()
    size = serializers.IntegerField()
    language = serializers.CharField()
    has_issues = serializers.BooleanField()
    has_projects = serializers.BooleanField()
    has_downloads = serializers.BooleanField()


class RepoDetailSerializer(RepoSerializer):
    stargazers_count = serializers.IntegerField()
    watchers_count = serializers.IntegerField()
    network_count = serializers.IntegerField()
    subscribers_count = serializers.IntegerField()


class UserSerializer(serializers.Serializer):
    login = serializers.CharField()
    id = serializers.IntegerField()
    node_id = serializers.CharField()
    avatar_url = serializers.CharField()
    html_url = serializers.CharField()
    type = serializers.CharField()


class UserDetailSerializer(UserSerializer):
    name = serializers.CharField()
    location = serializers.CharField()
    public_repos = serializers.IntegerField()
    public_gists = serializers.IntegerField()
    followers = serializers.IntegerField()
    following = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
