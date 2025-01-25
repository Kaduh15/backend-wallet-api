from decimal import Decimal
from rest_framework import serializers
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "user", "balance"]
        read_only_fields = [
            "id",
            "user",
            "balance",
        ]  # O usuário e saldo não podem ser alterados diretamente


class AddBalanceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),  # Agora 0.01 é um Decimal
    )


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.user.username")
    receiver = serializers.ReadOnlyField(source="receiver.user.username")

    class Meta:
        model = Transaction
        fields = ["id", "sender", "receiver", "amount", "timestamp"]
