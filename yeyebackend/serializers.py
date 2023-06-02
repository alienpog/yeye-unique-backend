from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    modelimages = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Products
        fields = ["id","name","price","old_price", "image", "modelimages"]

    def get_modelimages(self, obj):
        images = Crop_pictures.objects.filter(product=obj)
        return [image.image.url for image in images][0:3]

class ProductDetailsSerializer(serializers.ModelSerializer):
    crop_images = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Products
        fields = ["id","name","price","old_price", "image","description","crop_images"]

    def get_crop_images(self, obj):
        images = Crop_pictures.objects.filter(product=obj)
        return [image.image.url for image in images]
   

class CommentsSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    checkedlast= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comments
        fields = ["comment","user","image", "checkedlast"]

    def get_user(self, obj):
        return obj.user.name
    
    def get_comment(self, obj):
        return obj.comment
    
    def get_image(self, obj):
        return obj.user.image.url
    def get_checkedlast(self, obj):
        return obj.checkedlast
    
class TestimonialsSerializer(serializers.Serializer):
    client_picture = serializers.SerializerMethodField(read_only=True)
    client_name = serializers.SerializerMethodField(read_only=True)
    client_comment = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Testimonials

        fields =["client_comment","client_picture","client_name"]


    def get_client_picture(self, obj):
        return obj.client_picture.url
    
    def get_client_name(self, obj):
        return obj.client_name
    
    def get_client_comment(self, obj):
        return obj.client_comment

class VideosSerializer(serializers.Serializer):
    video= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model= videoPlayer

        fields =["video"]  

    def get_video(self, obj):
        return obj.video.url      
    

class LikesSerializer(serializers.Serializer):
    likescount= serializers.SerializerMethodField(read_only=True) 
    userliked= serializers.SerializerMethodField(read_only=True)  
    class Meta:
        models= Products
        fields =["likescount","userliked"]

    def get_likescount(self, obj):
        return obj.liked.count()   
    
    def get_userliked(self, obj):
        user = obj.liked.filter(liked__gmail=self.gmail)
        user= user.first()
        if user:
            return True
        return False
    

class GetingUserSerializer(serializers.Serializer):
    name= serializers.SerializerMethodField(read_only=True) 
    gmail= serializers.SerializerMethodField(read_only=True)  
    
    class Meta:
        models = Users
        fields=["name","gmail"]  

    def get_name(self,obj):
        return obj.name
    
    def get_gmail(self,obj):
        return obj.gmail
