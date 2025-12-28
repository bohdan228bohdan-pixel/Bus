from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['created_at']
