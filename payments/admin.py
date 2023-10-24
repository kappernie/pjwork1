from django.contrib import admin
from . import models


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'renter',
                    'property', 'currency', 'amount', 'settled', 'settlement_date']


@admin.register(models.PaymentSubscription)
class PaymentSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['down_payment', 'customer',
                    'plan', 'status', 'subscription_code', 'email_token', 'start_date', 'num_of_payments_made', 'next_payment_date']


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['property', 'plan_code', 'amount',
                    'down_payment_amt', 'interval', 'invoice_limit', 'description']

# _models = apps.get_app_config('payments').get_models()

# for model in _models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
