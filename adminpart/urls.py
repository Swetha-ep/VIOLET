from django.urls import path
from . import views

urlpatterns = [

    path('userlist',views.userlist,name='userlist'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    
    path('productlist',views.productlist,name='productlist'),
    path('categorylist',views.categorylist,name='categorylist'),
    path('searchcat',views.searchcat,name='searchcat'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('addproduct',views.addproduct,name='addproduct'),
    
    path('editcategory/<slug:slug>/', views.editcategory, name='editcategory'),
    path('editproduct/<slug:slug>/', views.editproduct, name='editproduct'),
    

]
