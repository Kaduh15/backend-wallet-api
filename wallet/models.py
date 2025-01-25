from django.db import models
from django.conf import settings


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Carteira de {self.user.username} - Saldo: {self.balance}"


class Transaction(models.Model):
    sender = models.ForeignKey(
        Wallet, related_name="sent_transactions", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Wallet, related_name="received_transactions", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.user.username} → {self.receiver.user.username}: R$ {self.amount}"
