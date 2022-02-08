from rest_framework import serializers
from .models import Buyer, BuyerAddress, BuyerCard,\
    BuyerWishlist, BuyerCart, ShippingCountries,\
    Coupon, Invoice, Order, ReturnProduct
from django.contrib.auth.hashers import make_password, check_password
import re
import stripe
from rest_framework.exceptions import ValidationError
import stripe
from Product.models import ProductVariant
from ecommerce.settings import STRIPE_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY


# Creating Buyer And Admin Serializer
class BuyerCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Buyer
        fields = '__all__'
        read_only_fields = ('user_ptr',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Save everything with lower case
    def validate(self, data):
        if data.get('email'):
            data['email'] = data.get('email').lower()
        if data.get('username'):
            data['username'] = data.get('username').lower()
        if data.get('gender'):
            data['gender'] = data.get('gender').lower()
        if data.get('password'):
            data['password'] = make_password(data.get('password'))
        data['is_active'] = True

        superuser = data.get('superuser')
        if superuser:
            data['is_superuser'] = True
        if data['is_superuser']:
            data['is_staff'] = True
        return data


# Buyer Serializer
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
        extra_kwargs = {'buyer': {'required': False}, }

    def validate(self, data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            data['buyer'] = request.user
        else:
            raise ValidationError({'authentication': 'You are not authenticated'})
        return data


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
    buyer = serializers.CharField(required=False)

    class Meta:
        model = BuyerCart
        fields = '__all__'

    def validate(self, data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            data['buyer'] = request.user
        else:
            raise ValidationError({'authentication': 'You are not authenticated'})
        return data


class BuyerWishlistSerializer(serializers.ModelSerializer):
    buyer = serializers.CharField(required=False)

    class Meta:
        model = BuyerWishlist
        fields = '__all__'

    def validate(self, data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            data['buyer'] = request.user
        else:
            raise ValidationError({'authentication': 'You are not authenticated'})
        return data


class ShippingCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCountries
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ReturnProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnProduct
        fields = '__all__'

    def validate(self, data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            data['buyer'] = request.user
        else:
            raise ValidationError({'authentication': 'You are not authenticated'})
        return data


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
