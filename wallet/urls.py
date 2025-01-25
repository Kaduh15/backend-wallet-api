from django.urls import path
from .views import WalletDetailView, AddBalanceView, TransferView, TransactionListView

urlpatterns = [
    path("balance/", WalletDetailView.as_view(), name="wallet_balance"),
    path("add/", AddBalanceView.as_view(), name="add_balance"),
    path("transfer/", TransferView.as_view(), name="transfer"),
    path("transactions/", TransactionListView.as_view(), name="transaction_list"),
]
