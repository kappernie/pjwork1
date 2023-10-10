from django.contrib import admin
from . import models


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'renter',
                    'property', 'currency', 'amount', 'settled', 'settlement_date']

# _models = apps.get_app_config('payments').get_models()

# for model in _models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
