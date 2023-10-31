from django.contrib import admin
from django.db.models import Q
from django.apps import apps
from . import models


# @admin.register(models.Agent)
# class AgentAdmin(admin.ModelAdmin):
#     list_display = ['user', 'verified']


@admin.register(models.Lister)
class ListerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'business_document',
                    'onboarding_completed', 'classification']

    list_filter = ('onboarding_completed',
                   ('business_document', admin.EmptyFieldListFilter),)

    actions = ['mark_onboarding_completed']

    def mark_onboarding_completed(self, request, queryset):
        queryset.update(onboarding_completed=True)

    mark_onboarding_completed.short_description = "Mark selected records as onboarding completed"


class EmptyFieldListFilter(admin.SimpleListFilter):
    title = 'business document uploaded'
    parameter_name = 'business_document'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Yes'),
            ('0', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.exclude(business_document__exact='')
        if self.value() == '0':
            return queryset.filter(business_document__exact='')


@admin.register(models.Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'verified']


_models = apps.get_app_config('users').get_models()

for model in _models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
