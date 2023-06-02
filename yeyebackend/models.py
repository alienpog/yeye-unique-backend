from django.db import models

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
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gmail

#Products
class Products(models.Model):
    name= models.CharField(max_length=100)
    image= models.FileField()
    price= models.FloatField()
    old_price =models.FloatField(blank=True, null=True)
    liked= models.ManyToManyField(Users,blank=True)
    description= models.TextField(blank=True, null=True)
    gender= models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

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