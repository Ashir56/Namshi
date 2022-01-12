from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import Buyer, BuyerAddress, BuyerCard, BuyerWishlist, BuyerCart
from .serializer import BuyerSerializer, BuyerCreateSerializer, BuyerCardCreateSerializer, \
    BuyerAddressSerializer, BuyerCardSerializer, BuyerWishlistSerializer, BuyerCartSerializer
import jwt
from rest_framework_jwt.settings import api_settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Create your views here.
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class BuyerAPI(GenericAPIView):
    serializer_class = BuyerSerializer

    def post(self, request):
        self.serializer_class = BuyerCreateSerializer
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            buyer = serializer.save()
            payload = jwt_payload_handler(buyer)
            print(payload)
            token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
            if buyer.is_superuser is True:
                return Response({"success": True, "id": buyer.id,
                                 "Msg": "Admin Created Successfully"}, status=status.HTTP_200_OK)
            return Response({"success": True, "token": token,
                             "msg":"Buyer Created Successfully"}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            buyer_id = request.query_params['id']
            buyer = Buyer.objects.get(uid=buyer_id)
            serializer = BuyerSerializer(buyer)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"success": False, "Msg": "User Does Not Exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
            buyer_id = self.request.query_params['id']
            buyer = Buyer.objects.get(uid=buyer_id)
            serializer = BuyerSerializer(buyer, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"success": True, "msg": "User Updated"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            buyer_id = request.query_params['id']
            buyer = Buyer.objects.get(uid=buyer_id)
            buyer.delete()
            return Response({"success": True, "msg": "Buyer Deleted"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ISADMIN(GenericAPIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = 'pbkdf2_sha256$320000$KuVaYeKylMbLGSGAAu05lO$pjwE1YIPqVfkiqajcSYnaUKm/wpBURdUzpINNUxcOGU='
            #password = request.data['password']
            print(username, password)
            user = Buyer.objects.filter(username=username, password=password)
            serializer = BuyerSerializer(user, many=True)
            print(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response("ERROR")


class ChangeStaffStatus(GenericAPIView):
    def post(self, request):
        try:
            userid = request.data['user_id']
            user = Buyer.objects.get(id=userid)
            if user.is_staff:
                user.is_staff = False
            else:
                user.is_staff = True
            user.save()
            return Response({"success": True, "msg": "Staff Status has been changed"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "User Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)


class BuyerAddressAPI(viewsets.ModelViewSet):
    queryset = BuyerAddress.objects.all()
    serializer_class = BuyerAddressSerializer
    permission_classes = [IsAuthenticated, ]


class BuyerCardAPI(viewsets.ModelViewSet):
    queryset = BuyerCard.objects.all()
    permission_classes = [IsAuthenticated, ]

    @property
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BuyerCardCreateSerializer
        else:
            return BuyerCardSerializer


class BuyerCartAPI(viewsets.ModelViewSet):
    queryset = BuyerCart.objects.all()
    serializer_class = BuyerCartSerializer
    permission_classes = [IsAuthenticated, ]


class BuyerWishlistAPI(viewsets.ModelViewSet):
    queryset = BuyerWishlist.objects.all()
    serializer_class = BuyerWishlistSerializer
    permission_classes = [IsAuthenticated, ]
