from django.contrib import admin
from .models import Account


class AccountModelAdmin(admin.ModelAdmin):
    list_display = ("date_joined", "username", "email", "is_superuser")


admin.site.register(Account, AccountModelAdmin)
