from django.contrib import admin

# Register your models here.

from .models import Aliment, Reteta, Plan, Cumparaturi

admin.site.register(Aliment)
admin.site.register(Reteta)
admin.site.register(Plan)
admin.site.register(Cumparaturi)