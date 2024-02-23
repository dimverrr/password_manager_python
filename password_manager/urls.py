from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title="Pastebin API")

urlpatterns = [
    path("", views.index, name="index"),
    path("credentials/new", views.add_credentials, name="add-credentials"),
    path(
        "credentials/<str:credential_name>/update",
        views.update_credential,
        name="update-credentials",
    ),
    path(
        "credentials/<str:credential_name>/delete",
        views.delete_credentials,
        name="delete-credentials",
    ),
    path(
        "credentials/<str:credential_name>",
        views.get_one_credentials,
        name="one-user-credentials",
    ),
    path("credentials/", views.get_all_credentials, name="all-user-credentials"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("test_token", views.test_token),
]
