from django.contrib import admin

from .models import ModelA

# Register your models here.


@admin.register(ModelA)
class ModelAAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
