from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/credentials/new", views.add_credentials, name="add-credentials"),
    path(
        "api/credentials/<str:credential_name>/update",
        views.update_credential,
        name="update-credentials",
    ),
    path(
        "api/credentials/<str:credential_name>/delete",
        views.delete_credentials,
        name="delete-credentials",
    ),
    path(
        "api/credentials/<str:credential_name>",
        views.get_one_credentials,
        name="one-user-credentials",
    ),
    path(
        "api/credentials/all/", views.get_all_credentials, name="all-user-credentials"
    ),
    path("api/login", views.login, name="login"),
    path("api/signup", views.signup, name="signup"),
    path("api/test_token", views.test_token),
]
