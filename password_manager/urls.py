from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title="Pastebin API")

urlpatterns = [
    path("api/", views.index, name="index"),
    path("api/credentials/new", views.add_credentials, name="create-credentials"),
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
        name="get-one-user-credentials",
    ),
    path(
        "api/credentials/", views.get_all_credentials, name="get-all-user-credentials"
    ),
    path("api/login", views.login, name="login"),
    path("api/signup", views.signup, name="signup"),
]
