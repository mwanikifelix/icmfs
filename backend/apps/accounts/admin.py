from django.contrib import admin
from .models import AbstractUser
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role",)


class SponsorAdmin(admin.ModelAdmin):
    list_display = ("company_name", "email", "status", "created_at")
    search_fields = ("company_name", "email")
    list_filter = ("status",)