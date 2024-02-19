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


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"Passed for {}".format(request.user.username)})


def index(request):
    return Response(
        {"Hello, world. You're at the polls index."}, status=status.HTTP_200_OK
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
                    "password": request.data["password"],
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
            password=request.data["password"],
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
    return Response({"creds": serializer.data}, status=status.HTTP_200_OK)


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
    return Response({"creds": serializer.data}, status=status.HTTP_200_OK)
