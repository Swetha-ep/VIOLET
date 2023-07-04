from ctypes import cast
import datetime
from io import BytesIO
from venv import logger
from autoslug import AutoSlugField
from django.db.models import DateField
from datetime import datetime,timedelta
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Product , Size , Offer
from cart.models import OrderItem, Order,Coupon
from .models import *
from django.utils.text import slugify
from django.views import View
from .decorators import superuser_required
from django.template.defaultfilters import slugify
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BannerForm, CouponForm,OfferForm
from app.models import Banner
from django.core.paginator import Paginator
from django.db.models.functions import TruncDay
from django.db.models import Sum
from django.db.models.functions import Cast
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from reportlab.platypus import SimpleDocTemplate, Table
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus.tables import TableStyle  # noinspection PyUnusedLocal

# Rest of your code



# Create your views here.

@superuser_required
def userlist(request):
     users_data = User.objects.all().order_by('id')
     return render(request, 'userlist.html', {'users': users_data})

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
    paginator = Paginator(products,9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    return render(request,'productlist.html',{'products':paged_products})


@superuser_required
def categorylist(request):
    categories = Category.objects.all()
    paginator = Paginator(categories,2)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    return render(request,'categorylist.html',{'categories':paged_categories})


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
        offer = request.POST.get['offer']

        
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
            offer = offer,
        )

        sizes = request.POST.getlist('sizes')
        product.sizes.set(sizes)

        return render(request, 'productlist', {'message': 'Product created successfully.'})

    categories = Category.objects.all()
    sizes = Size.objects.all()
    offer = Offer.objects.all()
    return render(request, 'addproduct.html', {'categories': categories, 'sizes': sizes, 'offer' : offer})


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



@superuser_required
def create_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('bannerlist')
    else:
        form = BannerForm()
    
    return render(request, 'addbanner.html', {'form': form})


@superuser_required
def edit_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('bannerlist')
    else:
        form = BannerForm(instance=banner)
    
    return render(request, 'editbanner.html', {'form': form, 'banner': banner})


def deletebanner(request, banner_id):
    banner =Banner.objects.get(id=banner_id)
    banner.delete()
    
    # if request.method == 'POST':
    #     banner.delete()
    #     return redirect('bannerlist')
    return redirect('bannerlist')


@superuser_required   
def banner_list(request):
    banners = Banner.objects.all()
    return render(request, 'bannerlist.html', {'banners': banners})


@superuser_required
def orderstatus(request):
    orders = OrderItem.objects.all()
    paginator = Paginator(orders,10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {'orders' : paged_products}
    return render(request,'orderstatus.html',context)



def update_status(request, order_item_id):
    order = Order.objects.get(id=order_item_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        # Redirect back to the same page or any desired page
        return redirect('orderstatus')  # Replace 'order_list' with your URL name


@superuser_required
def dashboard(request):

    delivered_items = Order.objects.filter(status='Delivered')

    revenue = 0
    for item in delivered_items:
        revenue += item.total_price

    top_selling = OrderItem.objects.annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = OrderItem.objects.all().order_by('-id')[:5]

    today = datetime.today()
    date_range = 7

    four_days_ago = today - timedelta(days=date_range)

    orders = Order.objects.filter(created_at__gte=four_days_ago, created_at__lte=today)

    sales_by_day = orders.annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
    sales_dates = Order.objects.annotate(sale_date=Cast('created_at', output_field=DateField())).values('sale_date').distinct()

    context = {
        'total_users':User.objects.count(),
        'sales':OrderItem.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
    }
    return render(request,'dashboard.html',context)

from datetime import datetime

def salesreport(request):
    
    context = {}
    if request.method == 'POST':
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        
        if start_date == '' or end_date == '':
            messages.error(request, 'Give date first')
            return redirect(salesreport)
            
        if start_date == end_date:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = OrderItem.objects.filter(order__created_at__date=date_obj.date())
            if order_items:
                context.update(sales=order_items, s_date=start_date, e_date=end_date)
                return render(request, 'salesreport.html', context)
            else:
                messages.error(request, 'No data found')
            return redirect(salesreport)

        order_items = OrderItem.objects.filter(order__created_at__date__gte=start_date, order__created_at__date__lte=end_date)

        if order_items:
            context.update(sales=order_items, s_date=start_date, e_date=end_date)
        else:
            messages.error(request, 'No data found')
        #Check if the user requested a download
    

    # if request.GET.get('download') == '1':
    #     # Generate the sales report data
    #     start_date = request.POST.get('start-date')
    #     end_date = request.POST.get('end-date')
    #     order_items = OrderItem.objects.filter(order__created_at__date__gte=start_date, order__created_at__date__lte=end_date)

    #     # Create a list to store the table data
    #     table_data = [['ID', 'Date', 'Customer', 'Product Name', 'Quantity', 'Total Price']]
    
    #     # Populate the table data with the relevant sales data
    #     for item in order_items:
    #         table_data.append([
    #             item.order.id,
    #             item.order.created_at.date(),
    #             item.order.address.customer,
    #             item.product.product_name,
    #             item.quantity,
    #             item.order.total_price
    #         ])

    #     # Create a PDF document
    #     buffer = BytesIO()
    #     doc = SimpleDocTemplate(buffer, pagesize=letter)
    #     elements = []

    #     # Create the table and set its style
    #     table = Table(table_data)
    #     table.setStyle(TableStyle([
    #         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #         ('FONTSIZE', (0, 0), (-1, 0), 12),
    #         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
    #     ]))

    #     # Add the table to the PDF document
    #     elements.append(table)

    #     # Build the PDF document
    #     doc.build(elements)

    #     # Set the appropriate response headers for downloading the PDF
    #     buffer.seek(0)
    #     response = HttpResponse(buffer, content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    #     return response

        
    return render(request, 'salesreport.html', context)

import csv

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no'])

    expenses = Order.objects.all()
    for expense in expenses:
        writer.writerow([expense.user, expense.total_price, expense.payment_mode,expense.tracking_no])

    return response


@superuser_required
def addcoupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('couponlist')
    else:
        form = CouponForm()
    
    return render(request, 'addcoupon.html', {'form': form})

@superuser_required
def editcoupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    
    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('couponlist')
    else:
        form = CouponForm(instance=coupon)
    
    return render(request, 'editcoupon.html', {'form': form, 'coupon': coupon})


@superuser_required   
def couponlist(request):
    coupon = Coupon.objects.all()
    return render(request, 'couponlist.html', {'coupon': coupon})


def deletecoupon(request, coupon_id):
    coupon =Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('couponlist')

def addoffer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('offerlist')
    else:
        form = OfferForm()
    
    return render(request, 'addoffer.html', {'form': form})

@superuser_required
def editoffer(request, offer_id):
    offer = get_object_or_404(offer, id=offer_id)
    
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('offerlist')
    else:
        form = OfferForm(instance=offer)
    
    return render(request, 'editoffer.html', {'form': form, 'offer': offer})

@superuser_required   
def offerlist(request):
    offer = Offer.objects.all()
    return render(request, 'offerlist.html', {'offer': offer})

def deleteoffer(request, offer_id):
    offer =Offer.objects.get(id=offer_id)
    offer.delete()
    return redirect('offerlist')