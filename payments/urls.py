from django.urls import path
from .views import OneTimePayment, RecurringPayment


urlpatterns = [
    path('onetime', OneTimePayment.as_view()),
    path('recurring', RecurringPayment.as_view()),
]
