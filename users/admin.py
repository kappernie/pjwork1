from django.contrib import admin
from django.apps import apps
from . import models


@admin.register(models.Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'verified']


@admin.register(models.Realtor)
class RealtorAdmin(admin.ModelAdmin):
    list_display = ['user', 'onboarding_completed']


@admin.register(models.Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ['user', 'verified']


_models = apps.get_app_config('users').get_models()

for model in _models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
