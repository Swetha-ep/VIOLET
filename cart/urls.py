from django.urls import path
from . import views

urlpatterns = [
    
    path('add-to-cart', views.addtocart, name="addtocart"),
    path('cart', views.cart, name="cart"),
    path('delete-cart-item',views.deletecartitem,name="deletecartitem"),
    path('wishlist',views.wishlist,name="wishlist"),
    path('addtowishlist',views.addtowishlist,name="addtowishlist"),
    path('delete-wish-item',views.deletewishitem,name="deletewishitem"),

    path('checkout',views.checkout,name='checkout'),
    path('place-order', views.placeorder, name="placeorder"),

    path('proceed-to-pay',views.razorpaycheck),

    path('my-orders', views.myorders,name="myorders"),
    path('view-order/<str:t_no>', views.orderview, name="orderview"),
]