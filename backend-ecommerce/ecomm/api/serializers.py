from rest_framework import serializers
from api.models import CustomerSignup,SellerSignup,Product,Cart,Order

class CustomerSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerSignup
        fields='__all__'

class SellerSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model=SellerSignup
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'

