from django.urls import path

from . import views
from api.views import ProductCreateView,GetProductsView,DeleteProductsView,UpdateProductsView,GetCartProductsView,DeleteCartsView,GoogleLoginApi
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
# router=routers.DefaultRouter()
# router.register('addproducts',ProductViewSet)

app_name = 'api'
urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('sellersignup/',views.sellersignup,name='sellersignup'),
    path('sellerlogin/',views.sellerlogin,name='sellerlogin'),
    path('addproducts/',views.ProductCreateView.as_view(),name='addproducts'),
    path('getproducts/<id>/',views.GetProductsView.as_view(),name="getproducts"),
    path('deleteproducts/<id>/',views.DeleteProductsView.as_view(),name='deleteproducts'),
    path('updateproducts/<id>/',views.UpdateProductsView.as_view(),name='updateproducts'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('deletecart/<id>/', views.DeleteCartsView.as_view(), name='remove_from_cart'),
    path('cart/<id>/', views.GetCartProductsView.as_view(), name='get_cart_items'),
    path('getproducts/',views.getproducts,name='getproducts'),
    path('createorder/',views.create_order,name='create_order'),
    path('singleproduct/<id>/',views.singleproduct,name='singleproduct'),
    path('myorder/<id>/',views.myorder,name='myorder'),
    path('v1/auth/login/google/',views.GoogleLoginApi.as_view(),name="google"),
    path('google-auth-callback/', views.google_auth_callback, name='google-auth-callback'),
    path('google-signin/',views.google_signin,name="google_signin"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)