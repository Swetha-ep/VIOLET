from django.urls import path
from . import views


urlpatterns = [
    
    path('add-to-cart', views.addtocart, name="addtocart"),
    path('cart', views.cart, name="cart"),
    path('update-cart',views.updatecart,name="updatecart"),
    path('delete-cart-item',views.deletecartitem,name="deletecartitem"),
    path('wishlist',views.wishlist,name="wishlist"),
    path('addtowishlist',views.addtowishlist,name="addtowishlist"),
    path('delete-wish-item',views.deletewishitem,name="deletewishitem"),

    path('checkout',views.checkout,name='checkout'),
    path('addaddress',views.addaddress,name="addaddress"),
    path('place-order', views.placeorder, name="placeorder"),

    path('user_profile/', views.UserProfileView, name='user_profile'),
    path('deleteprofile/<int:profile_id>',views.deleteprofile, name="deleteprofile"),
    path('editprofile/<int:profile_id>',views.editprofile, name='editprofile'),
    
    path('proceed-to-pay',views.razorpaycheck),

    path('my-orders', views.myorders,name="myorders"),
    path('view-order/<str:t_no>', views.orderview, name="orderview"),
    path('apply_coupon',views.apply_coupon,name="apply_coupon"),
    path('ordercancel/<int:order_id>',views.ordercancel,name='ordercancel'),
    path('order_return/<int:order_id>',views.order_return,name='order_return'), 
    

    
]
