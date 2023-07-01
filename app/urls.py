from django.urls import path
from . import views
from .views import loginn

urlpatterns = [
    
    path('',views.index,name='index'),
    path('<int:banner_id>/', views.index, name='index'),
    path('shop/',views.shop,name='shop'),  
    path('shop/<str:slug>/',views.collectionsview,name="collectionsview"), 
    path('collections/<str:cate_slug>/<str:prod_slug>',views.productview, name="productview"),
    path('register/',views.register,name="register" ),
    path('loginn/',views.loginn,name='loginn'),
    path('logout/',views.logout,name='logout'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    
]

    
