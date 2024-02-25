from .models import Credential
from .serializers import CredentialSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .utils import encrypt, decrypt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="post",
    request_body=UserSerializer,
)
@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Login"),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Password"
            ),
        },
    ),
    responses={200: "Success", 404: "Not found"},
)
@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["GET"])
def index(request):
    return Response({"Hello, world."}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    request_body=CredentialSerializer,
    operation_description="Create new credential object",
)
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_credentials(request):
    user_id = request.user
    serializer = CredentialSerializer(data=request.data)
    if serializer.is_valid():
        try:
            _, created = Credential.objects.get_or_create(
                credential_name=request.data["credential_name"],
                user=user_id,
                defaults={
                    "login": request.data["login"],
                    "password": encrypt(request.data["password"].encode("utf-8")),
                },
            )
            if created:
                return Response(
                    {"creds": serializer.data}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"Credentials with this name is already existing"},
                    status=status.HTTP_409_CONFLICT,
                )
        except ObjectDoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="put",
    request_body=CredentialSerializer,
    operation_description="Update credential object by credential name",
)
@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_credential(request, credential_name):
    user_id = request.user
    serializer = CredentialSerializer(data=request.data)
    if serializer.is_valid():
        updated = Credential.objects.filter(
            user_id=user_id, credential_name=credential_name
        ).update(
            credential_name=request.data["credential_name"],
            login=request.data["login"],
            password=encrypt(request.data["password"].encode("utf-8")),
        )
        if not updated:
            return Response(
                {"Credentials {} were not found".format(credential_name)},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"Credential {} were updated successfully".format(credential_name)},
            status=status.HTTP_200_OK,
        )


@swagger_auto_schema(
    method="delete",
    operation_description="Delete credential object by credential name",
)
@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_credentials(request, credential_name):
    user_id = request.user
    deleted, _ = Credential.objects.filter(
        user_id=user_id, credential_name=credential_name
    ).delete()
    if not deleted:
        return Response(
            {"Credentials {} were not found".format(credential_name)},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(
        {"Credential {} were deleted successfully".format(credential_name)},
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(
    method="get",
    operation_description="Get credential object by credential name",
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_one_credentials(request, credential_name):
    user_id = request.user
    creds = Credential.objects.filter(
        user_id=user_id, credential_name=credential_name
    ).first()
    if not creds:
        return Response(
            {"Credentials {} were not found".format(credential_name)},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = CredentialSerializer(creds)
    decrypted_password = decrypt(serializer.data["password"])
    return Response(
        {"creds": {"login": serializer.data["login"], "password": decrypted_password}},
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(
    method="get",
    operation_description="Get all user credential objects",
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_credentials(request):
    user_id = request.user
    creds = Credential.objects.filter(user_id=user_id).all()
    if not creds:
        return Response(
            {"User {} has no credentials".format(request.user.username)},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = CredentialSerializer(creds, many=True)
    return Response(
        {
            "creds": [
                {
                    "credential_name": creds["credential_name"],
                    "login": creds["login"],
                    "password": decrypt(creds["password"]),
                }
                for creds in serializer.data
            ]
        },
        status=status.HTTP_200_OK,
    )
