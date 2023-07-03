from django import forms
from app.models import Banner , Offer
from cart.models import Coupon

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image', 'title', 'description']
        

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'discount', 'minimum_purchase']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['offer_name', 'discount']