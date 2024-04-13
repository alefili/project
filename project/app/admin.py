from django.contrib import admin

# Register your models here.

from .models import Aliment, Plan

admin.site.register(Aliment)
admin.site.register(Plan)