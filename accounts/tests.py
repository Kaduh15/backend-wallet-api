from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from wallet.models import Wallet

User = get_user_model()


class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        self.user = User.objects.create_user(**self.user_data)
        
        # Criar carteira associada ao usuário
        self.wallet = Wallet.objects.create(user=self.user, balance=100.00)

    def test_register_user(self):
        """Testa o registro de um novo usuário"""
        new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post("/auth/register/", new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_user(self):
        """Testa o login de um usuário existente"""
        response = self.client.post(
            "/auth/login/",
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        response = self.client.post(
            "/auth/login/",
            {"username": self.user_data["username"], "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_route_without_token(self):
        """Testa acesso a uma rota protegida sem fornecer token JWT"""
        response = self.client.get("/wallet/balance/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_route_with_token(self):
        """Testa acesso a uma rota protegida com token JWT válido"""
        login_response = self.client.post(
            "/auth/login/",
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get("/wallet/balance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
