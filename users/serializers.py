from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Lister, Renter
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .helpermodule import send_realtor_account_creation_mail, send_renter_verification_mail
from property.models import Property
from rest_framework import serializers
from property.models import PropertyImage
from payments.models import Payment


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.IntegerField()  # 1: renter, 2: owner 3: agent
    phone = serializers.CharField()  # 1: renter, 2: owner 3: agent

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'user_type', 'first_name', 'last_name', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # first name and last name is required on sign up for a renter | validation handled on frontend |not required for realtor
        print(validated_data)
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError('User already exists')
        user_type = validated_data.pop('user_type', None)  # remove user type
        phone = validated_data.pop('phone', '')
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)  # create the user instance
        # depending on the type of user siging up
        if user_type == 1:
            Renter.objects.create(user=user, phone=phone)
            # send_realtor_account_creation_mail()
        elif user_type == 2:
            Lister.objects.create(user=user, phone=phone,
                                  classification='owner')
        elif user_type == 3:
            Lister.objects.create(user=user, phone=phone,
                                  classification='agent')
            # send_renter_verification_mail()
        # Assign the custom field to the user instance since it is a model serializer
        user.user_type = user_type
        user.phone = phone
        return user  # Return the instance, just like the original create() method


class RealtorBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lister
        fields = ['Bank_details']


class RealtorBusinessDoucmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lister
        fields = ['business_document']


class PropertySerializer(serializers.ModelSerializer):

    propertyimages = serializers.SerializerMethodField(required=False)
    property_types = serializers.StringRelatedField()
    lister_phone = serializers.SerializerMethodField(required=False)
    lister_id = serializers.SerializerMethodField(required=False)
    down_payment_amt = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)

    def get_propertyimages(self, obj):
        request = self.context.get('request')
        server_url = request.get_host()
        p_id = obj.id
        images = PropertyImage.objects.filter(property__id=p_id)
        # .values_list('upload', flat=True)
        imgs = ['http://' + server_url + i.upload.url for i in images]
        return imgs

    def get_lister_phone(self, obj):
        return obj.lister.phone if obj.lister.phone else 'Missing'

    def get_lister_id(self, obj):
        return obj.lister.pk if obj.lister.pk else 'Missing'

    class Meta:
        model = Property
        fields = ['pk', 'name', 'location_text', 'price', 'down_payment_amt', 'currency', 'for_rent', 'lister_phone', 'lister_id', 'min_rent_duration', 'max_rent_duration',
                  'description', 'Location', 'property_types', 'property_types_text', 'propertyimages']


class MultiplePropertyImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(
            max_length=100000, allow_empty_file=False, use_url=True)
    )


class TransactionsSerializer(serializers.ModelSerializer):
    # total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    # def get_total_amount(self, obj):
    #     # Add custom logic to calculate the total amount
    #     return obj.amount  # You can replace this with your calculation logic
