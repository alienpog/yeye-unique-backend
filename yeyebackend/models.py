from django.db import models
from django.template.defaultfilters import slugify 
# Create your models here.

#video
class videoPlayer(models.Model):
    title = models.CharField(max_length=100)
    video=models.FileField() 

    def __str__(self):
        return self.title
 
 
 #Users   
class Users(models.Model):
    name= models.CharField(max_length=50, blank=True, null=True)
    image= models.ImageField(blank=True, null=True)
    gmail= models.EmailField()
    phone= models.CharField(max_length=50, blank=True, null=True)
    complete= models.BooleanField(default=False)
    total_money = models.FloatField(default=0)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gmail

#Products
class Products(models.Model):
    name= models.CharField(max_length=100)
    image= models.FileField(blank=True, null=True)
    price= models.FloatField(blank=True, null=True)
    naira_price= models.FloatField(blank=True, null=True)
    old_dollar_price= models.CharField(max_length=200, blank=True, null=True)
    dollar_price= models.FloatField(blank=True, null=True)
    old_price =models.CharField(max_length=200, blank=True, null=True)
    currency= models.CharField(max_length=100, blank=True, null=True)
    zero_price = models.CharField(max_length=100, blank=True, null=True)
    liked= models.ManyToManyField(Users,blank=True)
    description= models.TextField(blank=True, null=True)
    description_span =models.TextField(blank=True, null=True)
    gender= models.CharField(max_length=50)
    hot= models.BooleanField(default=False)
    catalog= models.CharField(max_length=50, blank=True , null=True)
    special= models.BooleanField(default=False)
    materials_type= models.CharField(max_length=200, blank= True , null=True)
    Meta_Title = models.CharField(max_length=250, blank= True , null=True)
    Meta_description = models.TextField(blank=True, null=True)
    color= models.CharField(max_length=100, blank= True , null=True)
    slug= models.SlugField(blank=True, null=True)
    measurement = models.BooleanField(default=False)
    created_on= models.DateTimeField(auto_now_add=True)
    updated_on= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.slug
    
    def save(self,*args, **kwargs):
        to_assign=slugify(self.name)

        if Products.objects.filter(slug= to_assign).exists():
            to_assign=to_assign+str(Products.objects.all().count())

        self.slug=to_assign

        super().save(*args, **kwargs)    

#Crop_pictures
class Crop_pictures(models.Model):
    product= models.ForeignKey(Products, on_delete=models.CASCADE)   
    image= models.ImageField()
     
    def __str__(self):
        return self.product.name

#Comments
class Comments(models.Model):
    product= models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    user= models.ForeignKey(Users,on_delete=models.CASCADE,null=True, blank=True)  
    comment= models.TextField()
    checkedlast = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.product.name

# Testimonials   
class Testimonials(models.Model):
    client_name= models.CharField( max_length=200, null=True, blank=True)
    client_comment= models.TextField(null=True, blank=True) 
    client_picture= models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.client_name
    
# User Product Items
class ProductItems(models.Model):
    product= models.ForeignKey(Products,on_delete=models.CASCADE, null=True, blank=True)
    user= models.ForeignKey(Users, on_delete=models.CASCADE,null=True, blank=True)
    quantity= models.IntegerField(default=0)
    processing = models.BooleanField(default=False)

    @property
    def total_value(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.user.name + self.product.name
    
# User FreeGift
class FreeGift(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    price_to_pass = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.product.name
    
# UserClosed
class UserClosed(models.Model):
    place_of_delivery= models.TextField(blank=True, null=True)
    phone_number= models.CharField(max_length=100, blank=True,null=True)
    name= models.CharField(max_length=100,blank=True,null=True)
    all_total= models.FloatField(blank=True, null=True)
    email= models.EmailField(blank=True, null=True)
    product_items= models.ForeignKey(ProductItems,on_delete=models.CASCADE, null=True, blank=True)
    complete= models.BooleanField(default=False)
   
    def __str__(self):
      return self.name + self.email + self.phone_number
    