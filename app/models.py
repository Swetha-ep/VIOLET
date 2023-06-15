
from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth.models import User


import datetime
import os
# Create your models here.


def get_file_path(request,filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/',filename)

class Category(models.Model):

    slug = AutoSlugField(populate_from='category_name', unique=True)
    category_name = models.CharField(max_length=50, unique=True)
    cat_image = models.ImageField(upload_to=get_file_path, null= True, blank=True)
    description = models.CharField(max_length=500, null= False,blank=False)
    is_listed = models.BooleanField(default=True)

    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
        

    def __str__(self):
        return self.category_name

from django.db import models


class Size(models.Model):
    SIZE_CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )
    
    name = models.CharField(max_length=50, choices=SIZE_CHOICES)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='product_name', unique=True)
    product_name = models.CharField(max_length=200, unique=True)
    product_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    stock = models.IntegerField(null=False, blank=False, default=0)
    description = models.CharField(max_length=500, null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    is_available = models.BooleanField(default=True)
    trending = models.BooleanField(default=False, help_text="0=default, 1=trending")
    tag = models.CharField(max_length=150, null=False, blank=False)
    sizes = models.ManyToManyField('Size', related_name='products')  
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name



from django.db import models


class User_otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.BigIntegerField()
  
