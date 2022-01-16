from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import Buyer, BuyerAddress, BuyerCard, BuyerWishlist, BuyerCart
from .serializer import BuyerSerializer, BuyerCreateSerializer, BuyerCardCreateSerializer, \
    BuyerAddressSerializer, BuyerCardSerializer, BuyerWishlistSerializer, BuyerCartSerializer
import jwt
from rest_framework_jwt.settings import api_settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class BuyerAPI(GenericAPIView):
    serializer_class = BuyerSerializer

    def post(self, request):
        request.data._mutable = True
        name = ""
        if request.data.get('fullname'):
            name = request.data['fullname'].lower()
        fullname = name.split(' ')
        request.data['first_name'] = fullname[0]
        request.data['last_name'] = fullname[-1]
        serializer = BuyerCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            buyer = serializer.save()
            payload = jwt_payload_handler(buyer)
            token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
            request.data._mutable = False
            if buyer.is_superuser is True:
                return Response({"success": True, "id": buyer.id,
                                 "Msg": "Admin Created Successfully"}, status=status.HTTP_200_OK)
            return Response({"success": True, "token": token,
                             "msg": "Buyer Created Successfully"}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            buyer_id = request.query_params['id']
            buyer = Buyer.objects.get(id=buyer_id)
            serializer = BuyerSerializer(buyer)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"success": False, "Msg": "User Does Not Exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
            buyer_id = self.request.query_params['id']
            buyer = Buyer.objects.get(id=buyer_id)
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
            buyer = Buyer.objects.get(id=buyer_id)
            buyer.delete()
            return Response({"success": True, "msg": "User Deleted"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


# activate/deactivate a user
class ActivateDeactivateAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            user_id = request.GET.get('user_id')
            user = Buyer.objects.get(id=user_id)
            if user.is_superuser is True:
                raise Exception("You can not change another admin status")
            if user.is_active is True:
                user.is_active = False
                user.save()
                return Response({"success": True, "msg": "Requested user hase been deactivated"},
                                status=status.HTTP_200_OK)
            else:
                user.is_active = True
                user.save()
                return Response({"success": True, "msg": "Requested user hase been activated"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# search users
class SearchUser(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            name = request.data.get('name')
            if not name:
                raise Exception("Name field can not be None")
            buyer = Buyer.objects.filter(first_name=name) | Buyer.objects.filter(last_name=name) | \
                    Buyer.objects.filter(email=name) | Buyer.objects.filter(username=name)
            serializer = BuyerSerializer(buyer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
