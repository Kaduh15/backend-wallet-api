from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wallet.models import Wallet, Transaction
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Popula o banco de dados com usuários e transações fictícias"

    def handle(self, *args, **kwargs):
        # Criar 5 usuários fictícios
        users = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f"user{i}",
                defaults={"email": f"user{i}@example.com"}
            )
            if created:
                user.set_password("123456")
                user.save()
                Wallet.objects.create(user=user, balance=Decimal(random.uniform(50, 500)))

            users.append(user)

        self.stdout.write(self.style.SUCCESS("Usuários e carteiras criados com sucesso!"))

        # Criar transações aleatórias entre os usuários
        for _ in range(10):
            sender = random.choice(users)
            receiver = random.choice(users)
            while sender == receiver:
                receiver = random.choice(users)

            amount = Decimal(random.uniform(10, 100))
            sender_wallet = sender.wallet
            receiver_wallet = receiver.wallet

            if sender_wallet.balance >= amount:
                sender_wallet.balance -= amount
                receiver_wallet.balance += amount
                sender_wallet.save()
                receiver_wallet.save()

                Transaction.objects.create(sender=sender_wallet, receiver=receiver_wallet, amount=amount)

        self.stdout.write(self.style.SUCCESS("Transações fictícias criadas com sucesso!"))
