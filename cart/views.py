from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from django.contrib import messages
from app.models import Product,Category
import razorpay

from django.core.mail import send_mail

from .models import Cartt, Wishlist,Order,OrderItem,Profile,Coupon,CouponUsed,Wallet,Orderreturn
from app.views import *
import random


# <------------------------------------------cart management------------------------------------------------->
# <---------------------------------------------------------------------------------------------------------->

# Add to cart
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
            return JsonResponse({'status' : "Login to continue"})
        
    return redirect('/')


# cart page
@login_required(login_url='loginn')
def cart(request):
    cart = Cartt.objects.filter(user=request.user)
   
        
    context = {'cart': cart}
    return render(request, 'cart.html', context)



# cart updation
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


# delete cart
def deletecartitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if (Cartt.objects.filter(user=request.user,product_id=prod_id)):
            cartitem = Cartt.objects.get(product_id=prod_id,user=request.user)
            cartitem.delete()
        return JsonResponse({'status':"Cart item removed"})
    return redirect('/')

# <----------------------------------------------endofcart----------------------------------------------->

# <----------------------------------------------wishlist-------------------------------------------------->

# wishlist page
@login_required(login_url='loginn')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist' : wishlist}
    return render(request,'wishlist.html',context)


# add to wishlist
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


# delete wishlist
def deletewishitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if (Wishlist.objects.filter(user=request.user,product_id=prod_id)):
            wishlist = Wishlist.objects.get(product_id=prod_id,user=request.user)
            wishlist.delete()
        return JsonResponse({'status':"Wishlist item removed"})
    return redirect('/')

# <---------------------------------------------------endofwishlist----------------------------------------------->

# <---------------------------------------------------checkout---------------------------------------------------->

# checkout page
@login_required(login_url='loginn')
def checkout(request):
    cartitems = Cartt.objects.filter(user=request.user)
    
    total_price = 0
    for item in cartitems:
        if item.product.offer == None:
            total_price = total_price + item.product.selling_price * item.product_qty
        else:
            total_price = total_price + item.product.selling_price * item.product_qty - item.product.offer.discount

    userprofile = Profile.objects.filter(user=request.user).all()

    
    context = {'cartitems':cartitems, 'totalprice':total_price, 'userprofile' : userprofile}
        
    return render(request,'checkout.html',context)

# Add adress


@login_required

def addaddress(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')

        # Create a new profile object for the user
        profile = Profile.objects.create(
            user=request.user,
            fname=fname,
            lname=lname,
            phone=phone,
            address=address,
            city=city,
            state=state,
            country=country,
            pincode=pincode
        )

        messages.success(request, 'Profile added successfully')
        return redirect('user_profile')

    return render(request, 'add_profile.html')




# select address
def select_address(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selectedAddress')
        if selected_address_id:
            profile = Profile.objects.get(id=selected_address_id)
            
            return redirect('checkout',{'profile' : profile})  
    return redirect('checkout')  


# <----------------------------------------------------endofcheckout--------------------------------------------->


# <----------------------------------------------------placeorder------------------------------------------------->
#
# placeorder
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginn')
def placeorder(request):
    if request.method == 'POST':

        neworder = Order()
        neworder.user = request.user
        address = request.POST.get('address')
        a = Profile.objects.get(id=address)
        neworder.profile= a
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        new_price = request.POST.get('new_price')
        coupon_code2 = request.POST.get('coupon_code2')
        cart = Cartt.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            if item.product.offer == None:

                cart_total_price = cart_total_price +item.product.selling_price * item.product_qty
            else:
                cart_total_price = cart_total_price +item.product.selling_price * item.product_qty - item.product.offer.discount
        if new_price:
            print(new_price)
            cart_total_price = new_price

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
        current_user = request.user
        email = current_user.email
        mess=f'Hooray!\t{current_user.username},\nOrder confirmed! You are now part of the VIOLET family, where fashion is a way of life. Get ready to rock your style with confidence.\n We are thrilled to have you as part of our fashion-forward community!'
        send_mail(
                "VIOLET : Yay! Order Confirmed",
                mess,
                settings.EMAIL_HOST_USER,
                [current_user.email],
                fail_silently=False
            )
        messages.success(request,"Your order has been placed successfully")

        payMode = request.POST.get('payment_mode')
        if (payMode == "Paid by Razorpay"):
            return JsonResponse({'status':"Your order has been placed successfully."})
        if (payMode == "COD"):
            return JsonResponse({'status':"Your order has been placed successfully."})

    return redirect('myorders')

# <-----------------------------------------------------endofplaceorder-------------------------------------------------------->


# <-----------------------------------------------------userprofile----------------------------------------------------------->

# profile view
@login_required
def UserProfileView(request):
    profile = Profile.objects.filter(user=request.user)
    wallet = Wallet.objects.filter(user= request.user).first()
    return render(request, 'user_profile.html', {'profile' : profile, 'wallet' : wallet})




def editprofile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        
        profile.fname = fname
        profile.lname = lname
        profile.phone = phone
        profile.address = address
        profile.city = city
        profile.state = state
        profile.country = country
        profile.pincode = pincode
        profile.save()
        
        messages.success(request, 'Profile updated successfully')
        return redirect('user_profile')
    
    return render(request, 'user_profile.html', {'profile': profile})


def deleteprofile(request, profile_id):
    profile =Profile.objects.get(id=profile_id)
    profile.delete()
    return redirect('user_profile')
# <-------------------------------------------------------endofprofile--------------------------------------------------------->


# <-------------------------------------------------------ordermanagement------------------------------------------------------>

# order list
@login_required(login_url='loginn')
def myorders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders':orders
    }
    return render(request,'myorders.html', context)


# order view
@login_required(login_url='loginn')
def orderview(request,t_no):
    try :
        order = Order.objects.get(tracking_no = t_no)
    except Order.DoesNotExist:
        return redirect('myorders')
    orderitems = OrderItem.objects.filter(order = order)
    context = {
        'order':order,
        'orderItems':orderitems
    }
    return render(request,'orderview.html',context)


# cancel order
def ordercancel(request, order_id):
    order_item = OrderItem.objects.filter(order__id=order_id)
    for order_item in order_item:
        qty = order_item.quantity
        pid = order_item.product.id
        
        
        if order_item.order.payment_mode == 'Paid by Razorpay':
            order = Order.objects.get(id=order_id)
            total_price = order.total_price

            try:
                wallet = Wallet.objects.get(user=request.user)
                wallet.wallet += total_price
                wallet.save()
            except Wallet.DoesNotExist:
                wallet = Wallet.objects.create(user=request.user, wallet=total_price)
        
        if order_item.order.status == 'cancelled':
            messages.error(request, 'Order is already cancelled')
        
        else:
            order_item.order.status = "cancelled"
            order_item.quantity = 0
            order_item.save()
            order_item.order.save()
            messages.success(request, 'Order has been cancelled successfully')
            
    product = Product.objects.filter(id=pid).first()
    product.stock =product.stock + qty
    product.save()
    return redirect('myorders')


# order return
def order_return(request, order_id):
    order_item = OrderItem.objects.filter(order__id=order_id)
    
    try:
        order_return = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'order_not_found')
        return redirect('myorders')
    
    for order_item in order_item:
        if order_item.order.status == 'Return':
                messages.error(request, 'Order has already returned')
        else:
                order_item.order.status = "Return"
                order_item.order.save()
                messages.success(request, 'Order will be returned')

    if request.method == 'POST':
        comment = request.POST.getlist('comment')
        
        order_return = Orderreturn.objects.create(
            user=request.user,
            order=order_return,
            comment=comment,
            
        )
    return redirect('myorders')
# <-----------------------------------------------------endoforder-------------------------------------------------------------->


# <-------------------------------------------------razorpay--------------------------------------------------------------------->

# payment
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginn')
def razorpaycheck(request):
    cart = Cartt.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        if item.product.offer == None:
            total_price = total_price + item.product.selling_price * item.product_qty
        else:
            total_price = total_price + item.product.selling_price * item.product_qty - item.product.offer.discount

    return JsonResponse({

        'total_price' : total_price,
        # 'coupon_code2' : coupon_code2,
    }) 

# <--------------------------------------------------------endofrazorpay--------------------------------------------------->


# coupon
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        order_total = request.POST.get('order_total')
        print(coupon_code,order_total,"swethaaa")
        order_total = float(order_total)
        coupon = Coupon.objects.filter(coupon_code=coupon_code).first()
        print(coupon,"ansite")

        if coupon:
            coupon_used = CouponUsed.objects.filter(coupon_id=coupon.id)
            if coupon_used:
                return JsonResponse({'status': 'Coupon already used..'})
            else:
                if order_total > coupon.minimum_purchase:
                    new_total = order_total - coupon.discount
                    print(new_total)
                    return JsonResponse({'status': 'Coupon Applied..!!','new_total': new_total,'coupon_discount': coupon.discount, 'coupon_code': coupon_code})
                else:
                   return JsonResponse({'status': 'You can not use this coupon..'}) 
        else:
            return JsonResponse({'status': 'Coupon does not exist..'})



