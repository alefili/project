from django.contrib import admin

# Register your models here.

from .models import Aliment, Reteta, Plan, PlanReteta, PlanAliment, RetetaAliment

admin.site.register(Aliment)
admin.site.register(Reteta)
admin.site.register(Plan)
admin.site.register(PlanAliment)
admin.site.register(PlanReteta)
admin.site.register(RetetaAliment)