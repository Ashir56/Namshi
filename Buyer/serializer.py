from rest_framework import serializers
from .models import Buyer, BuyerAddress, BuyerCard,\
    BuyerWishlist, BuyerCart
import re
import stripe
from ecommerce.settings import STRIPE_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY

class BuyerCreateSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=100)

    class Meta:
        model = Buyer
        fields = '__all__'
        read_only_fields = ('user_ptr',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        name = data.get('fullname')
        fullname = name.split(' ')
        data['first_name'] = fullname[0]
        data['last_name'] = fullname[-1]
        superuser = data.get('superuser')
        if superuser:
            data['is_superuser'] = True
        if data['is_superuser']:
            data['is_staff'] = True
        return data

    def create(self, validated_data):
        user = Buyer(
            email=validated_data['email'],
            username=validated_data['username'],
            gender=validated_data['gender'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=validated_data['is_staff'],
            is_superuser=validated_data['is_superuser'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'
        read_only_fields = ('user_ptr',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class BuyerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerAddress
        fields = '__all__'


class BuyerCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerCard
        fields = '__all__'

    def validate(self, data):
        expiry_date = data.get('expiry_date')
        expiry = expiry_date.strftime('%Y-%m-%d')
        exp_year = re.split('-', expiry)

        token = stripe.Token.create(
            card={
                "number": data.get('card_number'),
                "exp_month": exp_year[1],
                "exp_year": exp_year[0],
                "cvc": data.get('cvc_num'),
            },
        )

        customer = stripe.Customer.create(
            source=token,
            description="My First Test Customer (created for API docs)",
        )
        data['token'] = customer.stripe_id
        return data


class BuyerCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerCard
        fields = '__all__'


class BuyerCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerCart
        fields = '__all__'


class BuyerWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerWishlist
        fields = '__all__'
