from django.urls import path

from . import views
from register.views import ProductViewSet,ProductCreateView,GetProductsView
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
router=routers.DefaultRouter()
router.register('addproducts',ProductViewSet)
urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('sellersignup/',views.sellersignup,name='sellersignup'),
    path('sellerlogin/',views.sellerlogin,name='sellerlogin'),
    path('addproducts/',views.ProductCreateView.as_view(),name='addproducts'),
    path('getproducts/<id>/',views.GetProductsView.as_view(),name="getproducts"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)