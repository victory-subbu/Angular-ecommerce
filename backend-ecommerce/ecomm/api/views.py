from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from api.models import CustomerSignup,SellerSignup,Product,Cart,Order
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.serializers import CustomerSignupSerializer,SellerSignupSerializer,ProductSerializer,CartSerializer,OrderSerializer
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static

from urllib.parse import urlencode

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect

# from api.mixins import ApiErrorsMixin, PublicApiMixin


# from auth.services import google_get_access_token, google_get_user_info
import requests
import base64
import os
import uuid



from django.http import JsonResponse
from google.oauth2 import id_token
from google.auth.transport import requests
# Create your views here.
@api_view(['POST'])
def signup(request):
        
        userdataserializer=CustomerSignupSerializer(data=request.data)
        if(userdataserializer.is_valid()):
            userdataserializer.save()
            print(userdataserializer)
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(userdataserializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(email,password)
    try:
        user_obj = CustomerSignup.objects.get(email=email, password=password)
        data={"userid": user_obj.userid,"name": user_obj.name}
        print(user_obj,user_obj.userid)
        return Response(data, status=status.HTTP_200_OK)
    except CustomerSignup.DoesNotExist:
        data={}
        return Response({'name': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def sellersignup(request):
        
        userdataserializer=SellerSignupSerializer(data=request.data)
        if(userdataserializer.is_valid()):
            userdataserializer.save()
            print(userdataserializer)
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(userdataserializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sellerlogin(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(email,password)
    
    try:
        user_obj = SellerSignup.objects.get(email=email, password=password)
        # If the user exists, you can return a success response
        data={"userid": user_obj.sellerid,"name": user_obj.name}
        print(user_obj,user_obj.sellerid)
        return Response(data, status=status.HTTP_200_OK)
    except SellerSignup.DoesNotExist:
        data={}
        # If the user does not exist, you can return an error response
        return Response({'name': 'Invalid login credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
#     def post(self, request, *args,**kwargs):
#         productname=request.data['productname']
#         productprice=request.data['productprice']
#         productcolor=request.data['productcolor']
#         productcategory=request.data['productcategory']
#         productdescription=request.data['productdescription']
#         productimage=request.data['productimage']
#         print(productname,productimage)
#         Product.pbjects.create(productname=productname,productprice=productprice,productcolor=productcolor,productcategory=productcategory,productdescription=productdescription,productimage=productimage)
#         # print(request.data)
#         # serializer = ProductSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         return HttpResponse({'message':'Product added'}, status=201)
        # return Response(serializer.errors, status=400)

class ProductCreateView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        seller=request.data['sellerid']
        productname=request.data['productname']
        productprice=request.data['productprice']
        productcolor=request.data['productcolor']
        productcategory=request.data['productcategory']
        productdescription=request.data['productdescription']
        productimage=request.data['productimage']
        try:
            sellerinstance= SellerSignup.objects.get(sellerid=seller)
        except SellerSignup.DoesNotExist:
            return HttpResponse({'error': 'Seller not found'}, status=404)
        print(productname,productimage)
        Product.objects.create(seller=sellerinstance,productname=productname,productprice=productprice,productcolor=productcolor,productcategory=productcategory,productdescription=productdescription,productimage=productimage)
        # print(request.data)
        # serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        return HttpResponse({'message':'Product added'}, status=201)
    
class GetProductsView(APIView):
     parser_classes=[MultiPartParser]
     def get(self,request,id):
        # sellerid=request.data['sellerid']
        products = Product.objects.filter(seller__sellerid=id)  
        serializer=ProductSerializer(products,many=True)
        product_data = []
        for product in products:
                product_details = {
                     'productid': product.productid,
                    'productname': product.productname,
                    'productprice': product.productprice,
                    'productcolor': product.productcolor,
                    'productcategory': product.productcategory,
                    'productdescription': product.productdescription,
                    'productimage':  product.productimage
                }
                product_data.append(product_details)
            
        return Response(serializer.data)

class DeleteProductsView(APIView):
    parser_classes=[MultiPartParser]
    def delete(self,request,id):
        product=Product.objects.get(productid=id)
        product.delete()
        return Response({'message':'Product deleted'})
    

class UpdateProductsView(APIView):
    parser_classes=[MultiPartParser]
    def put(self,request,id):
        product=Product.objects.get(productid=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def add_to_cart(request):
    cart_data = request.data
    print(request.data)
    customer_id = cart_data.get('userid')
    product_name = cart_data.get('productname')
    product_price = cart_data.get('productprice')
    product_color = cart_data.get('productcolor')
    product_category = cart_data.get('productcategory')
    product_description = cart_data.get('productdescription')
    product_image = cart_data.get('productimage')

    if not product_price:
        return Response({'message': 'Product price is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        customer = CustomerSignup.objects.get(userid=customer_id)
    except CustomerSignup.DoesNotExist:
        return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    
    Cart.objects.create(customer=customer,product_name=product_name,product_price=product_price,product_color=product_color,product_category=product_category,product_description=product_description,product_image=product_image)
    
    return Response({'message': 'Item added to cart successfully'})

@api_view(['DELETE'])
def remove_from_cart(request, customer_id):
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        cart.delete()
        return Response({'message': 'Item removed from cart successfully'})
    except Cart.DoesNotExist:
        return Response({'error': 'Cart does not exist'}, status=404)
    
# @api_view(['GET'])
# def get_cart_items(request,id):
#     user_id = request.GET.get('id')
#     print(user_id)  # Assuming you pass the user_id as a query parameter
#     if not user_id:
#         return Response({'message': 'Product price is required'}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         customer_instance=CustomerSignup.objects.get(userid=user_id)
#         cart_items = Cart.objects.filter(customer=customer_instance)
#         serializer = CartSerializer(cart_items, many=True)
#         return Response(serializer.data)
#     except Cart.DoesNotExist:
#         return Response({'message': 'Cart items not found.'}, status=404)
    
   
class GetCartProductsView(APIView):
     parser_classes=[MultiPartParser]
     def get(self,request,id):
             # Assuming you pass the user_id as a query parameter
            if not id:
                return Response({'message': 'Product price is required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                customer_instance=CustomerSignup.objects.get(userid=id)
                cart_items = Cart.objects.filter(customer=customer_instance)
                serializer = CartSerializer(cart_items, many=True)
                return Response(serializer.data)
            except Cart.DoesNotExist:
                return Response({'message': 'Cart items not found.'}, status=404)
        # sellerid=request.data['sellerid']
        


@api_view(['GET'])
def getproducts(request):
    products = Product.objects.all()[:4]
    serializer=ProductSerializer(products,many=True)
    product_data = []
    for product in products:
                product_details = {
                     'productid': product.productid,
                    'productname': product.productname,
                    'productprice': product.productprice,
                    'productcolor': product.productcolor,
                    'productcategory': product.productcategory,
                    'productdescription': product.productdescription,
                    'productimage':  product.productimage
                }
                product_data.append(product_details)
            
    return Response(serializer.data)

class DeleteCartsView(APIView):
    parser_classes=[MultiPartParser]
    def delete(self,request,id):
        product=Cart.objects.get(cartid=id)
        product.delete()
        return Response({'message':'Cart deleted'})
    
@api_view(['POST'])
def create_order(request):
    order_list = request.data  # Assuming it's a list of JSON objects
    print(order_list)
    for order_data in order_list:
        print(order_data)
        total_price = order_data.get('totalprice', 0) 
        serializer = OrderSerializer(data=order_data)
        customer_instance=CustomerSignup.objects.get(userid=order_data['customer'])
        Order.objects.create(customer=customer_instance,cartid=order_data['cartid'],product_name=order_data['product_name'],product_price=order_data['product_price'],product_color=order_data['product_color'],product_category=order_data['product_category'],product_description=order_data['product_description'],product_image=order_data['product_image'],total_price=total_price)
        if serializer.is_valid():
            print(2)
            serializer.save()

    return Response("Orders created successfully", status=201)

@api_view(['GET'])
def singleproduct(request,id):
     productid=id
     product=Product.objects.get(productid=productid)
     serializer=ProductSerializer(product)
     return Response(serializer.data)

@api_view(['GET'])
def myorder(request,id):
     orderid=id
     orderdata=Order.objects.filter(orderid=orderid)
     serializer=OrderSerializer(orderdata,many=True)
     return Response(serializer.data)





class GoogleLoginApi(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        # login_url = f'{settings.BASE_FRONTEND_URL}/login'

        # if error or not code:
        #     params = urlencode({'error': error})
        #     return redirect(f'{login_url}?{params}')

        domain = 'http://127.0.0.1:8000/'
        # api_uri = reverse('google')
        redirect_uri= 'http://127.0.0.1:8000/api/v1/auth/login/google/'

        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        profile_data = {
            'email': user_data['email'],
            'first_name': user_data.get('givenName', ''),
            'last_name': user_data.get('familyName', ''),
        }

        # Check if the user already exists in your system based on the email
        created=0

        if not created:
            # User already exists, redirect to the home page
            return redirect('http://localhost:43775/')

        # User is newly created, perform any additional logic or actions you need
        response= redirect('http://localhost:43775/')
        # response = redirect(settings.http://localhost:43775/)

        return response


def google_get_access_token(*, code: str, redirect_uri: str) -> str:
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://www.googleapis.com/oauth2/v4/token'
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
    data = {
        'code': code,
        'client_id': '814250556942-e04vlakebp5ebcc4nhdj3kq1dag8bba0.apps.googleusercontent.com',
        'client_secret': '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',
        'redirect_uri': redirect_uri,
        'grant_type': 'client_credentials'
    }
    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
    print(response)
    if not response.ok:
        raise Exception('Failed to obtain access token from Google.')

    access_token = response.json()['access_token']

    return access_token

     

def google_auth_callback(request):
    # Retrieve the ID token from the request
    token = request.POST.get('id_token', None)
    
    # Verify the ID token
    try:
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), '814250556942-e04vlakebp5ebcc4nhdj3kq1dag8bba0.apps.googleusercontent.com')
            
        # Extract relevant user information from id_info and authenticate the user in Django
        
        return JsonResponse({'success': True})
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid token'})
    
def google_signin(request):
    id_token = request.POST.get('id_token')
    CLIENT_ID = '814250556942-e04vlakebp5ebcc4nhdj3kq1dag8bba0.apps.googleusercontent.com'

    try:
        # Verify the token and get the user information
        info = id_token.verify_oauth2_token(id_token, requests.Request(), CLIENT_ID)

        # Process the user information as needed
        user_id = info['sub']
        email = info['email']
        # ...

        return JsonResponse({'success': True, 'message': 'Sign in with Google successful'})
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid token'})


    











     


# Create your views here.

    

     




    











     


# Create your views here.
