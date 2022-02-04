import json
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import Buyer, BuyerAddress, BuyerCard, BuyerWishlist, BuyerCart, \
    ShippingCountries, Coupon, Order, ReturnProduct, Invoice
from .serializer import BuyerSerializer, BuyerCreateSerializer, BuyerCardCreateSerializer, \
    BuyerAddressSerializer, BuyerCardSerializer, BuyerWishlistSerializer, BuyerCartSerializer, \
    ShippingCountriesSerializer, CouponSerializer, OrderSerializer, ReturnProductSerializer, InvoiceSerializer
import jwt
from django.db import transaction
from Product.models import Product, ProductVariant, Category
from rest_framework_jwt.settings import api_settings
from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.core.mail import EmailMessage
from ecommerce import settings
from HTML2PDF.utils import render_to_pdf
import datetime
from django.core.files import File
from io import BytesIO

# Create your views here.
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


# API creating/updating/deleting Buyer and Admin as well
class BuyerAPI(GenericAPIView):
    serializer_class = BuyerSerializer

    # Creating Buyer And Admin
    def post(self, request):
        request.data._mutable = True
        name = ''
        # Splitting name in first and last name
        if request.data.get('fullname'):
            name = request.data['fullname'].lower()
        fullname = name.split(' ')
        request.data['first_name'] = fullname[0]
        request.data['last_name'] = fullname[-1]
        # Posting in database through serializer
        serializer = BuyerCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            buyer = serializer.save()
            # Creating a Jwt token with custom payload for buyer
            payload = jwt_payload_handler(buyer)
            token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
            request.data._mutable = False
            if buyer.is_superuser is True:
                return Response({"success": True, "id": buyer.id,
                                 "Msg": "Admin Created Successfully"}, status=status.HTTP_200_OK)
            return Response({"success": True, "token": token,
                             "msg": "Buyer Created Successfully"}, status=status.HTTP_200_OK)

    # Retrieving Buyer and Admin from ids through parameter
    def get(self, request):
        try:
            buyer_id = request.query_params['id']
            buyer = Buyer.objects.get(id=buyer_id)
            serializer = BuyerSerializer(buyer)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"success": False, "Msg": "Buyer Does Not Exist"},
                            status=status.HTTP_404_NOT_FOUND)

    # Updating Buyer or Admin
    def patch(self, request):
        try:
            buyer_id = self.request.query_params['id']
            buyer = Buyer.objects.get(id=buyer_id)
            # Partially updating Buyer or Admin
            serializer = BuyerSerializer(buyer, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"success": True, "msg": "Buyer Updated"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Deleting buyer or admin
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


# Changing Staff Status of any instance from buyer model with their id
class ChangeStaffStatus(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            userid = request.data['user_id']
            user = Buyer.objects.get(id=userid)
            # Changing status
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
class ActivateDeactivateUserAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            user_id = request.GET.get('user_id')
            user = Buyer.objects.get(id=user_id)
            # If Buyer Activate then Deactivate him/her and vice versa
            if user.is_superuser is True:
                raise Exception("You can not change another admin status")
            if user.is_active is True:
                user.is_active = False
                user.save()
                return Response({"success": True, "msg": "Requested user hase been deactivated"},
                                status=status.HTTP_200_OK)
            else:
                user.is_active = True
                # Saving buyer with different active status in db
                user.save()
                return Response({"success": True, "msg": "Requested user hase been activated"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# search users through name or email or username
class SearchUser(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            name = request.data.get('name')
            if not name:
                raise Exception("Name field can not be None")
            # Searching user on the basis of first name, last name, username and email
            buyer = Buyer.objects.filter(first_name=name) | Buyer.objects.filter(last_name=name) | \
                    Buyer.objects.filter(email=name) | Buyer.objects.filter(username=name)
            serializer = BuyerSerializer(buyer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Adding/Updating/Deleting Buyer Address
class BuyerAddressAPI(viewsets.ModelViewSet):
    queryset = BuyerAddress.objects.all()
    serializer_class = BuyerAddressSerializer
    permission_classes = [IsAuthenticated, ]


# Adding/Updating/Deleting Buyer Card
class BuyerCardAPI(viewsets.ModelViewSet):
    queryset = BuyerCard.objects.all()
    permission_classes = [IsAuthenticated, ]

    @property
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BuyerCardCreateSerializer
        else:
            return BuyerCardSerializer


# Adding/Updating/Deleting Buyer Cart
class BuyerCartAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        with transaction.atomic():
            buyer = request.user
            carts = BuyerCart.objects.filter(buyer=buyer)

            product_quantity = int(request.data.get('product_quantity'))
            product_variant_id = request.data.get('product_variant')
            product_id = request.data.get('product')
            product = Product.objects.get(product_id=product_id)
            product_variant = ProductVariant.objects.get(id=product_variant_id, product=product)
            # Check if the desired product already exist in cart
            if carts is not None:
                for cart in carts:
                    if cart.product == product and cart.product_variant == product_variant:
                        return Response({"success": False, "msg": "Product is already in your cart"},
                                        status=status.HTTP_200_OK)
            # Checking if asked quantity to add in cart is more than what available in stock
            if product_quantity > product_variant.quantity:
                return Response({"success": False, "msg": "We don't have that many of this product in stock"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # Adding Product to Cart through serializer along with buyer id from request
            serializer = BuyerCartSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            # Decrementing quantity of product added to cart from available stock
            product_variant.quantity -= int(product_quantity)
            # Saving updating quantity of product in db
            product_variant.save()
            return Response({"success": True, "msg": "Product Added to Cart"}, status=status.HTTP_200_OK)

    # Updating only Quantity of product in cart
    def patch(self, request):
        cart_id = request.GET.get('cart_id')
        cart = BuyerCart.objects.get(buyerCart_id=cart_id)
        quantity = int(request.data.get('product_quantity'))
        # Getting the Product Variant
        product_variant = ProductVariant.objects.get(product=cart.product, size=cart.product_size,
                                                     color=cart.product_color)
        # Adding old quantity from cart back to variant db
        product_variant.quantity += cart.product_quantity
        product_variant.save()
        # Checking if desired quantity again is more than quantity in stock
        if quantity > product_variant.quantity:
            return Response({"success": False, "msg": "We don't have that many of this product in stock"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Updating the cart
        serializer = BuyerCartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        # Decrementing new quantity from product quantity available in stock
        product_variant.quantity -= quantity
        # Saving the updated variant in db
        product_variant.save()
        return Response({"success": True, "msg": "Product Updated in Cart"}, status=status.HTTP_200_OK)

    # Deleting the cart
    def delete(self, request):
        cart_id = request.GET.get('cart_id')
        cart = BuyerCart.objects.get(buyerCart_id=cart_id)
        product_variant = ProductVariant.objects.get(id=cart.product_variant.id)
        # Adding the quantity in cart to product variant quantity before deleting
        product_variant.quantity += int(cart.product_quantity)
        product_variant.save()
        # Deleting the cart
        cart.delete()
        return Response({"success": True, "msg": "Cart Deleted"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieving Single Cart from id through params
    def get(self, request):
        cart_id = request.GET.get('cart_id')
        cart = BuyerCart.objects.get(buyerCart_id=cart_id)
        if cart:
            serializer = BuyerCartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"success": False, "msg": "Cart Does not exist"}, status=status.HTTP_404_NOT_FOUND)


# Buyer Wishlist API (adding/updating/retrieving/deleting)
class BuyerWishlistAPI(viewsets.ModelViewSet):
    queryset = BuyerWishlist.objects.all()
    serializer_class = BuyerWishlistSerializer
    permission_classes = [IsAuthenticated, ]


# add/edit/delete shipping countries
class ShippingCountriesAPI(viewsets.ModelViewSet):
    queryset = ShippingCountries.objects.all()
    serializer_class = ShippingCountriesSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(ShippingCountriesAPI, self).get_permissions()


# add/edit/delete Coupons
class CouponAPI(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CouponSerializer


# OrderAPI (adding/updating/deleting/retrieving)
class OrderAPI(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]
    renderer_classes = [TemplateHTMLRenderer]

    # Creating an Order
    def post(self, request):
        with transaction.atomic():
            try:
                buyer = request.user
                buyer_address = BuyerAddress.objects.get(buyer=buyer)
                shipping_country = ShippingCountries.objects.get(country=buyer_address.country)
                coupon = Coupon.objects.get(country=shipping_country)
                buyer_coupon = 0
                # Checking if coupon exist for that country or not
                if coupon:
                    buyer_coupon = float(coupon.coupon)
                if buyer_address:
                    pass
                else:
                    return Response({"success": False, "msg": "You don't have any address"})
                carts = BuyerCart.objects.filter(buyer=buyer)
                # making lists to get grand total with discounts and shipping cost
                products = []
                colors = []
                sizes = []
                quantities = []
                discounted = []
                sub_total = 0
                # If cart exist
                if carts:
                    # Getting the Shipping Cost
                    try:
                        shipping_cost = shipping_country.shipping_cost
                    except ObjectDoesNotExist:
                        shipping_cost = 0
                    # Append Product, variant,quantities list
                    for cart in carts:
                        products.append(cart.product)
                        colors.append(cart.product_variant.color)
                        sizes.append(cart.product_variant.size.sizeID)
                        quantities.append(cart.product_quantity)
                    quantity_counter = 0
                    # Add Discount of each product in total sum
                    for product in products:
                        if product.discount_type == 'PE':
                            discounted_price = (product.product_discount * product.product_price) / 100
                            product_price = product.product_price - discounted_price
                        else:
                            product_price = product.product_price - product.product_discount
                        discounted.append(product_price)
                        products_sum = product_price * quantities[quantity_counter]
                        sub_total += products_sum

                        quantity_counter += 1

                    length = len(products)
                    # Check if length of all lists is equal
                    if any(len(lst) != length for lst in [colors, sizes, quantities]):
                        transaction.rollback()
                    product_id = []
                    for product in products:
                        product_id.append(product.product_id)
                    # making grand total with coupon discount and shipping cost
                    grand_total = sub_total + float(shipping_cost)
                    if coupon.coupon_type == 'PE':
                        coupon_discount = (float(buyer_coupon) * grand_total) / 100
                        grand_total -= coupon_discount
                    else:
                        grand_total -= buyer_coupon

                    # Creating order instance
                    order = Order.objects.create(products=str(product_id), colors=str(colors),
                                                 sizes=str(sizes), quantities=str(quantities), buyer=buyer,
                                                 grand_total=grand_total, shipping_cost=shipping_cost,
                                                 sub_total=sub_total, prices=json.dumps(discounted),
                                                 coupon=buyer_coupon)

                    # Deleting it from buyer's cart
                    carts.delete()
                    # Making an invoice template with context given below
                    invoice_list = zip(products, quantities, discounted)
                    context = {
                        "firstName": buyer.first_name.capitalize(),
                        "lastName": buyer.last_name.capitalize(),
                        "address": buyer_address.address,
                        "city": buyer_address.city,
                        "country": buyer_address.country,
                        "postal_code": buyer_address.postal_code,
                        "order": order,
                        "coupon": buyer_coupon,
                        "list": invoice_list,
                    }
                    # Creating index
                    invoice = Invoice.objects.create(order=order, buyer=buyer)
                    # converting invoice html template into pdf
                    pdf = render_to_pdf('invoice.html', context)
                    file = File(BytesIO(pdf.content))
                    invoice.invoice = file
                    # giving that template a name
                    invoice.invoice.name = '{}invoice.pdf'.format(order.order_id)
                    # Saving invoice
                    invoice.save()
                    return Response({"pdf": str(pdf)}, status=status.HTTP_200_OK)
                else:
                    return Response({"success": False, "msg": "Your cart is empty"}, status=status.HTTP_404_NOT_FOUND)
            except:
                transaction.rollback()

    # Retrieve all orders of buyer from authentication
    def get(self, request):
        orders = Order.objects.filter(buyer=request.user)
        if orders:
            ser = []
            for order in orders:
                order.colors = eval(order.colors)
                order.quantities = eval(order.quantities)
            serializer = OrderSerializer(orders, many=True)
            ser.append(serializer.data)
            return Response(ser, status=status.HTTP_200_OK)
        return Response({"success": False, "msg": "Buyer Does Not have any orders"},
                        status=status.HTTP_404_NOT_FOUND)


# Admin would be able to see each user’s current orders, order’s history and all the details of him/her.
class BuyerAndOrdersAPI(GenericAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            # Retrieving Buyer Through ID
            buyer_id = request.data.get('buyer')
            buyer = Buyer.objects.get(id=buyer_id)
            # Check if Buyer Exist
            if buyer:
                # Get all buyers Data from serializer
                ser = []
                serializer = BuyerSerializer(buyer)
                ser.append(serializer.data)
                # Getting all buyer's order through serializer
                buyer_orders = Order.objects.filter(buyer=buyer)
                # Check if buyer has any orders
                if buyer_orders:
                    # Retrieve each order through serializer and append the list
                    for buyer_order in buyer_orders:
                        serializer = OrderSerializer(buyer_order)
                        ser.append(serializer.data)
                    return Response(ser, status=status.HTTP_200_OK)
                return Response(ser, status=status.HTTP_200_OK)
            else:
                raise Exception('Buyer Does Not Exist')
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Change Status of Order and View Current Orders
class OrderTabAdminAPI(viewsets.ModelViewSet):
    queryset = Order.objects.filter(order_status=1)
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    # change status of order
    def create(self, request, *args, **kwargs):
        # get order id from parameters
        order_id = request.GET.get('order')
        order = Order.objects.get(order_id=order_id)
        # Check if order exist
        if order:
            order.order_status = request.data.get('status')
            order.save()
            return Response({"success": True, "msg": "Order's Status is changed"}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "msg": "Order Does Not Exist"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Number of Orders on a Specific Date
class OrderNumbersByDateAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Get date through request's body
        date = request.data.get('date')
        # Change only date in desired format
        datetime_object = datetime.datetime.strptime(date, '%Y/%m/%d').date()
        orders = Order.objects.filter(created_at__date=datetime_object)
        # Check if order exist
        if orders:
            return Response({"Total Number of Orders": orders.count()}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "msg": "No orders on that particular date"},
                            status=status.HTTP_400_BAD_REQUEST)


# Number of Orders by a Category
class OrderNumbersByCategoryAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Get Category through params
        category_id = request.data.get('category')
        category = Category.objects.get(category_id=category_id)
        if category:
            product = Product.objects.get(product_category=category)
            if product:
                # Filter through product list for desired id
                orders = Order.objects.filter(products__icontains=json.dumps(product.product_id))
                # Check if order exist
                if orders:
                    return Response({"Total Number of Orders": orders.count()}, status=status.HTTP_200_OK)
                else:
                    return Response({"success": False, "msg": "No orders for that category"},
                                    status=status.HTTP_400_BAD_REQUEST)


# Number of Orders by a Product
class OrderNumbersByProductAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        product = request.data.get('product')
        if product:
            orders = Order.objects.filter(products__icontains=json.dumps(product.product_id))
            if orders:
                return Response({"Total Number of Orders": orders.count()}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "msg": "No orders on that particular date"},
                                status=status.HTTP_400_BAD_REQUEST)


# Send invoice Email with invoice pdf
class SendEmailAPI(GenericAPIView):
    permission_classes = {IsAdminUser}

    def post(self, request):
        order_id = request.data.get('order')
        order = Order.objects.get(order_id=order_id)
        if order:
            invoice = Invoice.objects.get(order=order)
            pdf = invoice.invoice
            subject = request.data.get('subject')
            message = request.data.get('message')
            receiver = eval(request.data.get('receiver'))

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=receiver
            )
            email.attach("invoice.pdf", pdf.read())
            email.send(fail_silently=False)
            return Response({"success": True, "msg": "E-mail sent"}, status=status.HTTP_200_OK)


# Return Product from Order API
class ReturnProductAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        with transaction.atomic():
            try:
                # Get buyer from Request
                buyer = request.user
                # Get Buyer Address
                buyer_address = BuyerAddress.objects.get(buyer=buyer)
                # Check if Buyer Address Exist
                if buyer_address:
                    pass
                else:
                    return Response({"success": False, "msg": "Buyer Does Not have an interest"},
                                    status=status.HTTP_404_NOT_FOUND)
                # Get all the other required data from body
                quantity = int(request.data.get('quantity'))
                order_id = request.data.get('order')
                order = Order.objects.get(order_id=order_id)
                product_id = request.data.get('product')
                product = Product.objects.get(product_id=product_id)
                order_products = eval(order.products)
                if product.product_id not in order_products:
                    return Response({"success": False, "msg": "You never bought this product"},
                                    status=status.HTTP_404_NOT_FOUND)
                # Get Variant through id
                variant = request.data.get('variant')
                product_variant = ProductVariant.objects.get(id=variant, product=product)

                quantities = eval(order.quantities)
                sizes = eval(order.sizes)
                colors = eval(order.colors)
                counter = 0
                # Loop through Order's Product
                for order_product in order_products:
                    # Check if Product matches with product buyer wants to return
                    if product.product_id == order_product:
                        order_variant = ProductVariant.objects.get(product=product, color=colors[counter],
                                                                   size=sizes[counter])
                        # Check if Product variant matches with variant buyer wants to return
                        if product_variant == order_variant:
                            # Check if returning quantity is more than buyer ordered
                            if quantity > quantities[counter]:
                                return Response({"success": False, "msg": "returning more than you bought"},
                                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            if product.discount_type == 'PE':
                                discounted_price = (product.product_discount * product.product_price) / 100
                                product_price = product.product_price - discounted_price
                            else:
                                product_price = product.product_price - product.product_discount
                            # Change the grand_total and update the order instance
                            before_return_price = quantities[counter] * product_price
                            quantities[counter] -= quantity
                            after_return_price = product_price * quantities[counter]
                            order.sub_total -= before_return_price
                            order.sub_total += after_return_price
                            order.grand_total = order.sub_total + order.shipping_cost
                            order.quantities = json.dumps(quantities)
                            order.save()
                            # Add Product quantity he/she returned into variant stock
                            product_variant.quantity += quantity
                            product_variant.save()
                            price = product_price * quantity
                            # Creating the return product instance
                            ReturnProduct.objects.create(product=product, order=order, quantity=quantity,
                                                         buyer=buyer, price=price, variant=product_variant)
                            return Response({"success": True, "msg": "Product has been returned"},
                                            status=status.HTTP_200_OK)
                    counter += 1
                return Response({"success": False, "msg": "You never bought this product"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                print(e)
                transaction.rollback()
