from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from wallet.models import Wallet

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users",
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users",
        blank=True
    )

# Criar automaticamente uma Wallet quando um novo usuário for criado
@receiver(post_save, sender=CustomUser)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
