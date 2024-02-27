from .models import Credential
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.urls import reverse
from .utils import encrypt
from django.contrib.auth.hashers import make_password


class CredentialViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="test22222", password="testpass", email="test123@gmail.com"
        )
        self.user.save()
        self.token = Token.objects.create(user=self.user)

    def test_create_credentials(self):
        data = {
            "credential_name": "test_create",
            "login": "test1234@gmail.com",
            "password": "testpass",
            "user_id": self.user.id,
        }
        response = self.client.post(
            reverse("create-credentials"),
            data=data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Credential.objects.filter(credential_name="test_create").exists()
        )

    def test_update_credentials(self):
        credential = Credential.objects.create(
            credential_name="test_for_update",
            login="test123@gmail.com",
            password="testpass",
            user_id=self.user.id,
        )
        data = {
            "credential_name": "test_updated",
            "login": "test123@gmail.com",
            "password": "testpass",
            "user_id": 1,
        }
        response = self.client.put(
            reverse("update-credentials", args=[credential.credential_name]),
            data=data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        self.assertEqual(response.status_code, 200)
        credential.refresh_from_db()
        self.assertTrue(
            Credential.objects.filter(credential_name="test_updated").exists()
        )

    def test_delete_credentials(self):
        credential = Credential.objects.create(
            credential_name="test_for_delete",
            login="test123@gmail.com",
            password="testpass",
            user_id=self.user.id,
        )
        response = self.client.delete(
            reverse("delete-credentials", args=[credential.credential_name]),
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Credential.objects.filter(credential_name="test_for_delete").exists()
        )

    def test_get_one_credential(self):
        credential = Credential.objects.create(
            credential_name="test_for_get_one",
            login="test123@gmail.com",
            password=encrypt("testpass"),
            user_id=self.user.id,
        )
        response = self.client.get(
            reverse("get-one-user-credentials", args=[credential.credential_name]),
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["creds"]["password"], b"testpass")

    def test_get_all_credential(self):
        Credential.objects.create(
            credential_name="test_for_get_all1",
            login="test123@gmail.com",
            password=encrypt("testpass"),
            user_id=self.user.id,
        )
        Credential.objects.create(
            credential_name="test_for_get_all2",
            login="test123@gmail.com",
            password=encrypt("testpass"),
            user_id=self.user.id,
        )
        response = self.client.get(
            reverse("get-all-user-credentials"),
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["creds"]), 2)


class UserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="test_user",
            password=make_password("test_password"),
            email="test@gmail.com",
        )

    def test_signup(self):
        data = {
            "username": "test_user1",
            "password": "test_password",
            "email": "test123@test.com",
        }
        response = self.client.post(reverse("signup"), data=data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue("token" and "user_id" in response.data)

    def test_login(self):
        data = {"username": self.user.username, "password": "test_password"}
        response = self.client.post(reverse("login"), data=data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" and "user_id" in response.data)
