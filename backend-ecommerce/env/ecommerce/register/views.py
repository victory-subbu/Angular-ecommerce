from django.shortcuts import render
from django.http import HttpResponse
from register.models import CustomerSignup,SellerSignup,Product
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from register.serializers import CustomerSignupSerializer,SellerSignupSerializer,ProductSerializer
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
import base64
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
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def post(self, request, *args,**kwargs):
        productname=request.data['productname']
        productprice=request.data['productprice']
        productcolor=request.data['productcolor']
        productcategory=request.data['productcategory']
        productdescription=request.data['productdescription']
        productimage=request.data['productimage']
        print(productname,productimage)
        Product.pbjects.create(productname=productname,productprice=productprice,productcolor=productcolor,productcategory=productcategory,productdescription=productdescription,productimage=productimage)
        # print(request.data)
        # serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        return HttpResponse({'message':'Product added'}, status=201)
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
                    'productname': product.productname,
                    'productprice': product.productprice,
                    'productcolor': product.productcolor,
                    'productcategory': product.productcategory,
                    'productdescription': product.productdescription,
                    'productimage':  product.productimage
                }
                product_data.append(product_details)
            
        return Response(serializer.data)
     
# def get_product_image_url(productimage):
#         if productimage:
            
#             if productimage.storage == staticfiles_storage:
        
#                 return static(productimage.name)
#             else:
              
#                 return productimage.url
#         return None
       
     


