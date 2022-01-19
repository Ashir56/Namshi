from rest_framework import serializers
from .models import Buyer, BuyerAddress, BuyerCard,\
    BuyerWishlist, BuyerCart, ShippingCountries, Coupon
from django.contrib.auth.hashers import make_password, check_password
import re
import stripe
from ecommerce.settings import STRIPE_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY


class BuyerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'
        read_only_fields = ('user_ptr',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        data['email'] = data.get('email').lower()
        data['username'] = data.get('username').lower()
        data['gender'] = data.get('gender').lower()
        data['password'] = make_password(data.get('password'))

        superuser = data.get('superuser')
        if superuser:
            data['is_superuser'] = True
        if data['is_superuser']:
            data['is_staff'] = True
        if data['is_superuser']:
            data['is_active'] = True
        return data

    # def create(self, validated_data):
    #     user = Buyer(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #         gender=validated_data['gender'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #         is_staff=validated_data['is_staff'],
    #         is_superuser=validated_data['is_superuser'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'
        read_only_fields = ('user_ptr',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data.get('first_name'):
            data['first_name'] = data.get('first_name').lower()
        if data.get('last_name'):
            data['last_name'] = data.get('last_name').lower()
        if data.get('email'):
            data['email'] = data.get('email').lower()
        if data.get('username'):
            data['username'] = data.get('username').lower()
        if data.get('gender'):
            data['gender'] = data.get('gender').lower()
        return data


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


class ShippingCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCountries
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
