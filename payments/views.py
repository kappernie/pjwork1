from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
# Create your views here.

print(settings.PROPERTY_RECURRING_PAYMENT_PERCENTAGE)


class OneTimePayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        for_rent = request.query_params.get('for_rent')
        if for_rent == 'true':
            print(request.data)
            return Response('Onetime for rent')
        elif for_rent == 'false':
            print(request.data)
            return Response('Onetime not for rent')


class RecurringPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        for_rent = request.query_params.get('for_rent')
        if for_rent == 'true':
            print(request.data)
            return Response('Recurring for rent')
        elif for_rent == 'false':
            print(request.data)
            return Response('Recurring not for rent')
