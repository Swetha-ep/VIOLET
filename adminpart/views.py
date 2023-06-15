from venv import logger
from autoslug import AutoSlugField
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Product , Size
from .models import *
from django.utils.text import slugify
from django.views import View
from .decorators import superuser_required
from django.template.defaultfilters import slugify


# Create your views here.

@superuser_required
def userlist(request):
     users_data = User.objects.all()
     return render(request, 'userlist.html', {'users': users_data})


def user_profile(request, user_id):
    user_data = User.objects.get(id=user_id)   
    return render(request, 'user_profile.html', {'user': user_data})


@superuser_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginn')
def block_user(request,user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('userlist')


@superuser_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginn')
def unblock_user(request,user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('userlist')


def logout(request):
    return redirect('loginn')


@superuser_required
def productlist(request):
    products = Product.objects.all()
    return render(request,'productlist.html',{'products':products})


@superuser_required
def categorylist(request):
    categories = Category.objects.all()
    return render(request,'categorylist.html',{'categories':categories})


@superuser_required
def list_product(request, product_name):
    try:
        product = Product.objects.get(name=product_name)
        product.is_listed = True
        product.save()
        return redirect('product_list')  
    except Product.DoesNotExist:
        return redirect('product_list') 
    

@superuser_required
def unlist_product(request, product_name):
    try:
        product = Product.objects.get(id=product_name)
        product.is_listed = False
        product.save()
        return redirect('product_list')  
    except Product.DoesNotExist:
        return redirect('product_list')


@superuser_required
def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        cat_image = request.FILES.get('cat_image')
        description = request.POST.get('description')
        is_listed = request.POST.get('is_listed', False)

        # Generate the slug automatically
        slug = slugify(category_name)

        if not category_name:
            messages.error(request, "Fields can't be blank!!!")
            return redirect('addcategory')

        if Category.objects.filter(slug=slug).exists():
            messages.error(request, 'Category already exists')
            return redirect('addcategory')

        category = Category.objects.create(
            slug=slug,
            category_name=category_name,
            cat_image=cat_image,
            description=description,
            is_listed=True if is_listed == 'True' else False,
        )
        
        return redirect('categorylist',{'message': 'Category created successfully'})

    return render(request, 'addcategory.html')



@superuser_required
def editcategory(request, slug):
    category = Category.objects.get(slug=slug)
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        cat_image = request.FILES.get('cat_image')
        description = request.POST.get('description')
        is_listed = request.POST.get('is_listed') == 'on' 
        
        category.category_name = category_name
        category.cat_image = cat_image
        category.description = description
        category.is_listed = is_listed
        
        category.save()
        
        return redirect('categorylist',{'message': 'Category updated successfully'})
    
    return render(request, 'editcategory.html', {'category': category})


 
def searchcat(request):
    if request.method =='POST':
        searched = request.POST['searchvalue']
        
        category = Category.objects.filter(category_name = searched)

        if category.exists():
            return render(request,'searchcat.html',{'searched':searched,'category':category})    
        else:
           
            return redirect('categorylist',{'message': 'Category does not exist'})
        
    return render(request,'searchcat.html')


@superuser_required
def addproduct(request):
    if request.method == 'POST':
        category_slug = request.POST['category']
        category = Category.objects.get(slug=category_slug)
        product_name = request.POST['product_name']
        product_image = request.FILES['product_image']
        stock = request.POST['stock']
        description = request.POST['description']
        original_price = request.POST['original_price']
        selling_price = request.POST['selling_price']
        is_available = request.POST.get('is_available', False) == 'on'
        trending = request.POST.get('trending', False) == 'on'
        tag = request.POST['tag']

        
        slug = slugify(product_name)

        product = Product.objects.create(
            category=category,
            slug=slug,
            product_name=product_name,
            product_image=product_image,
            stock=stock,
            description=description,
            original_price=original_price,
            selling_price=selling_price,
            is_available=is_available,
            trending=trending,
            tag=tag,
        )

        sizes = request.POST.getlist('sizes')
        product.sizes.set(sizes)

        return render(request, 'productlist', {'message': 'Product created successfully.'})

    categories = Category.objects.all()
    sizes = Size.objects.all()
    return render(request, 'addproduct.html', {'categories': categories, 'sizes': sizes})


@superuser_required
def editproduct(request, slug):
    product = Product.objects.get(slug=slug)
    
    if request.method == 'POST':
        
        category_slug = request.POST.get('category')
        product_name = request.POST.get('product_name')
        product_image = request.FILES.get('product_image')
        sizes = request.POST.getlist('sizes')
        description = request.POST.get('description')
        is_available = request.POST.get('is_available') == 'on'
        stock = request.POST.get('stock')
        original_price = request.POST.get('original_price')
        selling_price = request.POST.get('selling_price')
        trending = request.POST.get('trending') == 'on'
        tag = request.POST.get('tag')
        
       
        product.category = Category.objects.get(slug=category_slug)
        product.product_name = product_name
        if product_image:
            product.product_image = product_image
        product.sizes.clear()
        for size_id in sizes:
            product.sizes.add(Size.objects.get(id=size_id))
        product.description = description
        product.is_available = is_available
        product.stock = stock
        product.original_price = original_price
        product.selling_price = selling_price
        product.trending = trending
        product.tag = tag
        product.save()
        
        
        return redirect('productlist', {'message': 'Product updated successfully.'})
    
    categories = Category.objects.all()
    sizes = Size.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'sizes': sizes
    }
    return render(request, 'editproduct.html', context)
