from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
# Create your views here.

print(settings.PROPERTY_RECURRING_PAYMENT_PERCENTAGE)

def verify_transaction():
    pass

class OneTimePayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        for_rent = request.query_params.get('for_rent')
        # verify transaction for this (outer function so I can reuse it)try except
        if for_rent == 'true':
            print(request.data)
            return Response('Onetime for rent')
            # create Payment record in db
        elif for_rent == 'false':
            print(request.data)
            # create Payment record in db
            return Response('Onetime not for rent')


class RecurringPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        for_rent = request.query_params.get('for_rent')
        # verify transaction for this (outer function so I can reuse it)try except
        if for_rent == 'true':
            print(request.data)
            # create payment record in db for initial upfront payment
            # create plan using paystack endpoint and certain agreed upon calculations
            # then create the subscription for the user
            # on success, create plan record in db, then subscription record in db
            return Response('Recurring for rent')
        elif for_rent == 'false':
            print(request.data)
            return Response('Recurring not for rent')
