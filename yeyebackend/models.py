from django.db import models

# Create your models here.

#Users
class Users(models.Model):
    name= models.CharField(max_length=50, blank=True, null=True)
    image= models.ImageField(blank=True, null=True)
    gmail= models.EmailField()
    phone= models.IntegerField()
    complete= models.BooleanField(default=False)

    def __str__(self):
        return self.gmail

#Products
class Products(models.Model):
    name= models.CharField(max_length=100)
    image= models.FileField()
    price= models.FloatField()
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
    product= models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    user= models.ForeignKey(Users,on_delete=models.SET_NULL,null=True, blank=True)  
    Comment= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.product.name

# Testimonials   
class Testimonials(models.Model):
    client= models.OneToOneField(Comments, on_delete=models.SET_NULL, null=True, blank=True)  

    def __str__(self) -> str:
        return self.client.user.name