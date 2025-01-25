from django.test import TestCase
from django.contrib.auth import get_user_model
from wallet.models import Wallet, Transaction
from decimal import Decimal

User = get_user_model()


class WalletTestCase(TestCase):
    def setUp(self):
        """Cria dois usuários com carteiras para os testes"""
        self.user1 = User.objects.create_user(username="user1", password="123456")
        self.user2 = User.objects.create_user(username="user2", password="123456")

        self.wallet1 = Wallet.objects.create(user=self.user1, balance=Decimal(100))
        self.wallet2 = Wallet.objects.create(user=self.user2, balance=Decimal(50))

    def test_wallet_creation(self):
        """Testa se as carteiras são criadas corretamente"""
        self.assertEqual(self.wallet1.balance, 100)
        self.assertEqual(self.wallet2.balance, 50)

    def test_transaction(self):
        """Testa se uma transferência é processada corretamente"""
        amount = Decimal(20)
        self.wallet1.balance -= amount
        self.wallet2.balance += amount
        self.wallet1.save()
        self.wallet2.save()

        Transaction.objects.create(
            sender=self.wallet1, receiver=self.wallet2, amount=amount
        )

        self.assertEqual(self.wallet1.balance, 80)
        self.assertEqual(self.wallet2.balance, 70)
