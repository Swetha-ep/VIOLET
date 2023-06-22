from django.urls import path
from . import views


urlpatterns = [

    path('userlist',views.userlist,name='userlist'),
    
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    
    path('productlist',views.productlist,name='productlist'),
    path('categorylist',views.categorylist,name='categorylist'),
    path('searchcat',views.searchcat,name='searchcat'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('addproduct',views.addproduct,name='addproduct'),
    
    path('editcategory/<slug:slug>/', views.editcategory, name='editcategory'),
    path('editproduct/<slug:slug>/', views.editproduct, name='editproduct'),

    path('addbanner', views.create_banner, name='addbanner'),
    path('editbanner/<int:banner_id>/', views.edit_banner, name='editbanner'),
    path('deletebanner/<int:banner_id>/', views.delete_banner, name='deletebanner'),
    path('bannerlist/', views.banner_list, name='bannerlist'),

    path('orderstatus', views.orderstatus,name='orderstatus'),
    path('update_status/<int:order_item_id>',views.update_status,name='update_status'),

    path('dashboard',views.dashboard,name="dashboard"),
     path('salesreport/',views.salesreport, name="salesreport"),
    path('export_csv/',views.export_csv, name="export_csv"),
    

]
