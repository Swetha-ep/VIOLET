from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from django.contrib import messages
from app.models import Product,Category


from .models import Cartt, Wishlist,Order,OrderItem,Profile
from app.views import *
import random



@login_required(login_url='loginn')
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('prod_id'))
            product_check = Product.objects.get(id = prod_id)
            if (product_check):
                if (Cartt.objects.filter(user=request.user.id, product_id = prod_id)):
                    return JsonResponse({'status':"Product already in cart"})
                else:
                    prod_qty = int(request.POST.get('prod_qty'))

                    if product_check.stock >= prod_qty:
                        Cartt.objects.create(user=request.user, product_id = prod_id, product_qty=prod_qty)
                        return JsonResponse({'status' : "Product added successfully"})
                    else:
                        return JsonResponse({'status':"Only"+ str(product_check.stock)+"quantity available"})
                    
            else:
                return JsonResponse({'status':"No such product found"})
        else:
            return JsonResponse({'status' : ""})
        
    return redirect('/')


@login_required(login_url='loginn')
def cart(request):
    cart = Cartt.objects.filter(user=request.user)

    context = {'cart': cart}
    return render(request, 'cart.html', context)


def updatecart(request):
    if request.method=='POST':
        prod_id = request.POST.get('prod_id')
        if(Cartt.objects.filter(user=request.user,product_id=prod_id)):
            prod_qty = int(request.POST.get('prod_qty'))
            cart = Cartt.objects.get(product_id=prod_id,user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"Updated Successfully"})
    return redirect('/')


def deletecartitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if (Cartt.objects.filter(user=request.user,product_id=prod_id)):
            cartitem = Cartt.objects.get(product_id=prod_id,user=request.user)
            cartitem.delete()
        return JsonResponse({'status':"Cart item removed"})
    return redirect('/')


@login_required(login_url='loginn')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist' : wishlist}
    return render(request,'wishlist.html',context)

def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = request.POST.get('prod_id')
            product_check = Product.objects.get(id = prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Product already in Wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id = prod_id)
                    return JsonResponse({'status':"Product added to Wishlist"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status':"Login to continue"})

    return redirect('/')

def deletewishitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if (Wishlist.objects.filter(user=request.user,product_id=prod_id)):
            wishlist = Wishlist.objects.get(product_id=prod_id,user=request.user)
            wishlist.delete()
        return JsonResponse({'status':"Wishlist item removed"})
    return redirect('/')


@login_required(login_url='loginn')
def checkout(request):
    cartitems = Cartt.objects.filter(user=request.user)
    
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()

    
    context = {'cartitems':cartitems, 'totalprice':total_price, 'userprofile' : userprofile}
        
    return render(request,'checkout.html',context)


@login_required(login_url='loginn')
def placeorder(request):
    if request.method == 'POST':

        currentuser = User.objects.filter(id=request.user.id).first()
        if not currentuser.username:
            currentuser.email = request.POST.get('email')
        
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.fname = request.POST.get('fname')
            userprofile.lname = request.POST.get('lname')
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cartt.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price +item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price
        trackno = 'violet'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no = trackno) is None:
             trackno = 'violet'+str(random.randint(1111111,9999999))
        
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cartt.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.selling_price,
                quantity = item.product_qty
            )
            orderproduct = Product.objects.filter(id=item.product.id).first()
            orderproduct.stock= orderproduct.stock - item.product_qty
            orderproduct.save()

        Cartt.objects.filter(user = request.user).delete()
        messages.success(request,"Your order has been placed successfully")

        payMode = request.POST.get('payment_mode')
        if (payMode == "Paid by Razorpay"):
            return JsonResponse({'status':"Your order has been placed successfully."})

    return redirect('/')



@login_required
def UserProfileView(request):
    user = request.user
    profile = Order.objects.filter(user=user)
    return render(request, 'user_profile.html',{'profile' : profile})



@login_required(login_url='loginn')
def myorders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {'orders':orders}
    return render(request,'myorders.html',context)


@login_required(login_url='loginn')
def orderview(request,t_no):
    order = Order.objects.filter(tracking_no = t_no).filter(user =request.user).first()
    orderitems = OrderItem.objects.filter(order = order)
    context = {
        'order':order,
        'orderItems':orderitems
    }
    return render(request,'orderview.html',context)


@login_required(login_url='loginn')
def razorpaycheck(request):
    
    cart = Cartt.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.product.selling_price * item.product_qty

    return JsonResponse({

        'total_price' : total_price
    }) 


