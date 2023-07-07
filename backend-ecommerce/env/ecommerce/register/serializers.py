from rest_framework import serializers
from register.models import CustomerSignup,SellerSignup,Product

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
        
