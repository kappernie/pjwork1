from decimal import Decimal
import requests
import json
from dateutil.relativedelta import relativedelta
from math import floor
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.utils import timezone
from property.models import Property
from users.models import Renter
from .models import Payment, PaymentSubscription, Plan
# Create your views here.

# print(settings.PROPERTY_RENT_RECURRING_PAYMENT_PERCENTAGE)
# print(settings.PROPERTY_BUY_RECURRING_PAYMENT_PERCENTAGE)


def verify_transaction(trxref):
    try:
        # Define the endpoint URL
        url = f"https://api.paystack.co/transaction/verify/{trxref}"

        # Define the headers for the API request
        headers = {
            # Replace with your Paystack Secret Key
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET}",
            "Content-Type": "application/json",
        }
        # Make the API request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            json_response = response.json()
            transaction_data = json_response.get('data')
            return transaction_data

        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that were raised
        print(f"An error occurred: {e}")


def create_plan(name, amount, interval, invoice_limit):
    # Define the endpoint URL
    url = "https://api.paystack.co/plan"

    # Define the headers for the API request
    headers = {
        # Replace with your Paystack Secret Key
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET}",
        "Content-Type": "application/json",
    }

    # Define the data for the new plan
    data = {
        "name": name,
        "amount": float(amount) * 100,
        "interval": interval,
        "invoice_limit": invoice_limit,
    }

    # Make the API request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check if the request was successful
        if response.status_code == 201:
            # Parse the JSON response
            json_response = response.json()

            # Get the plan data
            plan_data = json_response.get('data')

            # Return the plan data
            return plan_data

        else:
            # If the request was not successful, raise an exception
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that were raised
        print(f"An error occurred: {e}")


def create_subscription(customer, plan, start_date):
    # Define the endpoint URL
    url = "https://api.paystack.co/subscription"

    # Define the headers for the API request
    headers = {
        # Replace with your Paystack Secret Key
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET}",
        "Content-Type": "application/json",
    }

    # Define the data for the new subscription
    data = {
        "customer": customer,
        "plan": plan,
        "start_date": start_date.isoformat()
    }

    # Make the API request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_response = response.json()

            # Get the subscription data
            subscription_data = json_response.get('data')

            # Return the subscription data
            return subscription_data

        else:
            # If the request was not successful, raise an exception
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that were raised
        print(f"An error occurred: {e}")


class OneTimePayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        for_rent = request.query_params.get('for_rent')
        data = request.data
        if not data:
            return Response({'error': 'Supply the necessary data'}, status=status.HTTP_400_BAD_REQUEST)
        # verify transaction for this (outer function so I can reuse it)try except
        trx_verification_res = verify_transaction(data.get('reference'))
        # print(trx_verification_res)
        if for_rent == 'true':
            # print(request.data)
            if trx_verification_res.get('status') == 'success':
                # Get the renter
                renter = Renter.objects.get(
                    user__email=data.get('emailAddress'))

                # Get the property
                property = Property.objects.get(
                    pk=int(data.get('property_id', 0)))

                # Create a new Payment record
                payment = Payment(
                    renter=renter,
                    property=property,
                    amount=data.get('amount'),
                    settled=True,
                    duration=int(data.get('duration')),
                    settlement_date=timezone.now(),
                    currency=data.get('currency'),
                    transaction_id=data.get('reference'),
                    status='completed',
                )
                payment.save()

                return Response({'success': True, 'message': 'Payment verification successful', 'property_id': data.get('property_id'), 'payment_type': 'onetime_for_rent'})
            else:
                return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        elif for_rent == 'false':
            # print(request.data)

            if trx_verification_res.get('status') == 'success':
                # Get the renter
                renter = Renter.objects.get(
                    user__email=data.get('emailAddress'))

                # Get the property
                property = Property.objects.get(
                    pk=int(data.get('property_id', 0)))

                # Create a new Payment record
                payment = Payment(
                    renter=renter,
                    property=property,
                    amount=data.get('amount'),
                    settled=True,
                    settlement_date=timezone.now(),
                    currency=data.get('currency'),
                    transaction_id=data.get('reference'),
                    status='completed',
                )
                payment.save()

                return Response({'success': True, 'message': 'Payment verification successful', 'property_id': data.get('property_id'), 'payment_type': 'onetime_buying'})
            else:
                return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class RecurringPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        for_rent = request.query_params.get('for_rent')
        data = request.data
        if not data:
            return Response({'error': 'Supply the necessary data'}, status=status.HTTP_400_BAD_REQUEST)
        # verify transaction for this (outer function so I can reuse it)try except
        trx_verification_res = verify_transaction(data.get('reference'))
        # print(trx_verification_res)
        # print(trx_verification_res)
        if for_rent == 'true':
            # print(request.data)

            # create payment record in db for initial upfront payment
            if trx_verification_res is not None and trx_verification_res.get('status') == 'success':
                # Get the renter
                renter = Renter.objects.get(
                    user__email=data.get('emailAddress'))

                # Get the property
                property = Property.objects.get(
                    pk=int(data.get('property_id', 0)))

                duration = int(data.get('duration'))

                # Create a new Payment record
                payment = Payment.objects.create(
                    renter=renter,
                    property=property,
                    amount=data.get('amount'),
                    settled=True,
                    duration=duration,
                    settlement_date=timezone.now(),
                    currency=data.get('currency'),
                    transaction_id=data.get('reference'),
                    status='completed',
                )

                # create plan using paystack endpoint and certain agreed upon calculations
                # The upfront payment is for 6 months, per Ghana's Housing Laws
                remaining_months = int(data.get('duration')) - 6
                raw_interval = int(data.get('interval'))
                if raw_interval == Plan.QUARTERLY:
                    interval = 3  # in months
                    paystack_interval = 'quarterly'
                elif raw_interval == Plan.BIANUALLY:
                    interval = 6  # in months
                    paystack_interval = 'biannually'

                invoice_limit = floor(remaining_months / interval)
                total_amt_at_end_of_sub = remaining_months * property.price * \
                    Decimal(
                        str(1 + settings.PROPERTY_RENT_RECURRING_PAYMENT_PERCENTAGE))
                
                onetime_payment_amt = duration * property.price

                amt_per_sub_interval = total_amt_at_end_of_sub / invoice_limit
                
                plan_name = f'Recurring_4_Rent_{data.get("emailAddress")}_{property.pk}_limit_{invoice_limit}'

                plan_data = create_plan(
                    plan_name, amt_per_sub_interval, paystack_interval, invoice_limit)
                if plan_data:
                    plan = Plan.objects.create(
                        property=property,
                        plan_code=plan_data.get('plan_code'),
                        amount=amt_per_sub_interval,
                        down_payment_amt=data.get('amount'),
                        total_amount_at_the_end_of_sub=total_amt_at_end_of_sub,
                        onetime_payment_amt=onetime_payment_amt,
                        description=plan_name,
                        interval=raw_interval,
                        invoice_limit=invoice_limit,
                    )

                    # then create the subscription for the user
                    start_date = timezone.now() + relativedelta(months=6)
                    subscription_data = create_subscription(
                        data.get("emailAddress"), plan_data.get('plan_code'), start_date)
                    if subscription_data:
                        subscription = PaymentSubscription(
                            down_payment=payment,
                            customer=renter,
                            plan=plan,
                            subscription_code=subscription_data.get(
                                'subscription_code'),
                            email_token=subscription_data.get('email_token'),
                            start_date=start_date,
                            next_payment_date=start_date,
                        )

                        subscription.save()

                        return Response({'success': True, 'message': 'Payment verification successful', 'property_id': data.get('property_id'), 'payment_type': 'recurring_for_rent'})
                    else:
                        return Response({'error': 'Something went wrong when creating subscription'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error': 'Something went wrong when creating plan'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        elif for_rent == 'false':
            # print(request.data)
            # create payment record in db for initial upfront payment
            if trx_verification_res is not None and trx_verification_res.get('status') == 'success':
                # Get the renter
                renter = Renter.objects.get(
                    user__email=data.get('emailAddress'))

                # Get the property
                property = Property.objects.get(
                    pk=int(data.get('property_id', 0)))

                mortgageDuration = int(data.get('mortgageDuration', 12))

                # Create a new Payment record
                payment = Payment.objects.create(
                    renter=renter,
                    property=property,
                    amount=data.get('amount'),
                    settled=True,
                    settlement_date=timezone.now(),
                    currency=data.get('currency'),
                    transaction_id=data.get('reference'),
                    status='completed',
                )

                # create plan using paystack endpoint and certain agreed upon calculations
                # The upfront payment is for 6 months, per Ghana's Housing Laws
                remaining_amount = Decimal(
                    '0.7') * property.price  # upfront payment is 30%

                invoice_limit = mortgageDuration  # cos it is monthly.
                if mortgageDuration == 12:
                    percentage_amount = settings.PROPERTY_BUY_RECURRING_PAYMENT_PERCENTAGE
                elif mortgageDuration == 36:
                    percentage_amount = 3 * settings.PROPERTY_BUY_RECURRING_PAYMENT_PERCENTAGE
                elif mortgageDuration == 60:
                    percentage_amount = 5 * settings.PROPERTY_BUY_RECURRING_PAYMENT_PERCENTAGE

                total_amt_at_end_of_sub = remaining_amount * \
                    Decimal(
                        str(1 + percentage_amount))
                onetime_payment_amt = property.price

                amt_per_sub_interval = total_amt_at_end_of_sub / invoice_limit
                plan_name = f'Recurring_4_Buying_{data.get("emailAddress")}_{property.pk}_limit_{invoice_limit}'

                plan_data = create_plan(
                    plan_name, amt_per_sub_interval, 'monthly', invoice_limit)
                if plan_data:
                    plan = Plan.objects.create(
                        property=property,
                        plan_code=plan_data.get('plan_code'),
                        amount=amt_per_sub_interval,
                        down_payment_amt=data.get('amount'),
                        total_amount_at_the_end_of_sub=total_amt_at_end_of_sub,
                        onetime_payment_amt=onetime_payment_amt,
                        description=plan_name,
                        interval=3,
                        invoice_limit=invoice_limit,
                    )

                    # then create the subscription for the user
                    start_date = timezone.now() + relativedelta(months=1)
                    subscription_data = create_subscription(
                        data.get("emailAddress"), plan_data.get('plan_code'), start_date)
                    if subscription_data:
                        subscription = PaymentSubscription(
                            down_payment=payment,
                            customer=renter,
                            plan=plan,
                            subscription_code=subscription_data.get(
                                'subscription_code'),
                            email_token=subscription_data.get('email_token'),
                            start_date=start_date,
                            next_payment_date=start_date,
                        )

                        subscription.save()

                        return Response({'success': True, 'message': 'Payment verification successful', 'property_id': data.get('property_id'), 'payment_type': 'recurring_buying'})
                    else:
                        return Response({'error': 'Something went wrong when creating subscription'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error': 'Something went wrong when creating plan'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
