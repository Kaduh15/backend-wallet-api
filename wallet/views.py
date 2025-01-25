from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Wallet, Transaction
from .serializers import WalletSerializer, AddBalanceSerializer, TransactionSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@permission_classes([IsAuthenticated])
class SecureView:
    pass


class WalletDetailView(generics.RetrieveAPIView):
    """Consulta o saldo da carteira do usuário autenticado"""

    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet


class AddBalanceView(generics.UpdateAPIView):
    """Adiciona saldo à carteira do usuário"""

    serializer_class = AddBalanceSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            wallet = request.user.wallet
            wallet.balance += amount
            wallet.save()
            return Response(
                {"message": "Saldo adicionado com sucesso", "balance": wallet.balance},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferView(generics.CreateAPIView):
    """Realiza uma transferência entre usuários"""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sender_wallet = request.user.wallet
        receiver_username = request.data.get("receiver")
        amount = request.data.get("amount")

        try:
            receiver_wallet = Wallet.objects.get(user__username=receiver_username)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Usuário destinatário não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if sender_wallet == receiver_wallet:
            return Response(
                {"error": "Você não pode transferir para si mesmo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount is None or float(amount) <= 0:
            return Response(
                {"error": "O valor da transferência deve ser maior que zero"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if sender_wallet.balance < float(amount):
            return Response(
                {"error": "Saldo insuficiente"}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            sender_wallet.balance -= float(amount)
            sender_wallet.save()

            receiver_wallet.balance += float(amount)
            receiver_wallet.save()

            transaction_record = Transaction.objects.create(
                sender=sender_wallet, receiver=receiver_wallet, amount=amount
            )

        return Response(
            TransactionSerializer(transaction_record).data,
            status=status.HTTP_201_CREATED,
        )


class TransactionListView(generics.ListAPIView):
    """Lista transações realizadas pelo usuário autenticado, com filtro opcional por período"""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_wallet = self.request.user.wallet
        queryset = Transaction.objects.filter(sender=user_wallet).order_by("-timestamp")

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])

        return queryset
