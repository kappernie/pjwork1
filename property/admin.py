from django.contrib import admin
from django.apps import apps
from . import models


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['country', 'Region', 'city', 'suburb']


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'lister', 'property_types', 'currency',
                    'price', 'location_text', 'location_modified', 'is_published']

    @admin.display(description='Location')
    def location_modified(self, obj):
        return f'{obj.Location.city} - {obj.Location.suburb}' if obj.Location else '-'


@admin.register(models.PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property_modified', 'upload']

    @admin.display(description='Property')
    def property_modified(self, obj):
        return f'{obj.property.name} - {obj.property.currency}{obj.property.price} - {obj.property.location_text}' if obj.property else '-'


@admin.register(models.PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['type']


_models = apps.get_app_config('property').get_models()

for model in _models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
