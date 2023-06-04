from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer ,TestimonialsSerializer,CommentsSerializer,VideosSerializer,ProductDetailsSerializer,GetingUserSerializer
from .models import *
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Create your views here.



# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))

class CustomPagination(PageNumberPagination):
    page_size = 12  # Number of items to display per page
    page_size_query_param = 'page_size'  # URL query parameter for overriding the page size


# puttin product in the database
def product_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                name= request.POST.get('name')
                priceold= request.POST.get('priceold')
                pricenew= request.POST.get('pricenew')
                description= request.POST.get('description')
                Image= request.FILES['Image']
                gender= request.POST.get('gender')
                Crop_Images = request.FILES.getlist('Crop_Images')
                print("images01>>>>>", Image)
                product = Products.objects.create(name=name,price=pricenew,old_price=priceold,description=description,image=Image,gender=gender)
                product.save()
                for image in Crop_Images:
                    crop_picture = Crop_pictures.objects.create(image=image, product=product)
                    crop_picture.save()
                    print("images>>>>>", image)
            except:
                print("not uploaded")     
        return render(request, 'index.html')
    return redirect('https://www.google.com')

# putting testimonal in the database
def testimonial_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                name= request.POST.get('name')
                comment= request.POST.get('comment')
                Image= request.FILES['Image']
                testimonial= Testimonials.objects.create(client_name=name, client_comment=comment, client_picture=Image)
                testimonial.save()
                print("images>>>>>", Image)
            except:
                    print("not uploaded") 
        return render(request, 'testimonial.html')
    return redirect('https://www.google.com')

def getting_all_customers(request):
    if request.user.is_authenticated:
        clients= Users.objects.all().order_by('-updated_at')
        return render(request, 'customers.html', {"clients":clients})
    return redirect('https://www.google.com')

# specific data of the product
@api_view(['GET'])
def products_details(request, pk):
    if pk=="none":
        queryset= Products.objects.all()
        serializer = ProductDetailsSerializer(queryset, many=True)
        return Response(serializer.data)
    person = Products.objects.filter(pk=int(pk))
    if not person.exists():
        return Response({},status=404)
    person=person.first()
    serializer = ProductDetailsSerializer(person, many=False)
    return Response(serializer.data)

# geting  all comments of a product
@api_view(['GET'])
def comments(request, pk):
    comments = Comments.objects.filter(product=pk).order_by('-checkedlast')
    serializer = CommentsSerializer(comments, many=True)
    return Response(serializer.data)

# collecting most liked products
@api_view(['GET'])
def mostliked(request):
    likedproducts = Products.objects.annotate(like_count=Count('liked')).order_by('-like_count')
    serializer = ProductSerializer(likedproducts, many=True)
    return Response(serializer.data)

# all testimony products
@api_view(['GET'])
def testimonials(request):
    clients = Testimonials.objects.all()
    serializer= TestimonialsSerializer(clients, many=True)
    return Response(serializer.data)

# video player
@api_view(['GET'])
def videoplayer(request):
    videos = videoPlayer.objects.all()
    serializer = VideosSerializer(videos, many=True)
    return Response(serializer.data)

# counting likes
@api_view(['GET'])
def likescount(request, pk):
    product = Products.objects.filter(id=pk)
    obj = product.first()
    number = obj.liked.count()
    return Response(number, status=200)

# when user clicks on a like and unlike button
@api_view(['POST'])
def postlike(request,pk):
    data = request.data or {}
    product = Products.objects.filter(id=pk)
    obj = product.first()
    email = data.get('email')
    user = Users.objects.filter(gmail=email)
    if user is None: 
        return Response(False, status=200)
    user= user.first()
    action = data.get('action')
    if action == 'like':
        obj.liked.add(user)
        return Response(True, status=200)
    if action == 'unlike':
        obj.liked.remove(user)
        return Response(False, status=200)

        
# checking if the user liked or not liked on first load
@api_view(['POST'])
def productlikes(request, pk):
    data =request.data or {}
    product = Products.objects.filter(id=pk)
    obj = product.first()
    email= data.get('email')
    user =Users.objects.filter(gmail=email)
    if user is None:
        return Response({"likes": False}, status=200)
    if user.first() in obj.liked.all():
        return Response( True, status=200)
    return Response( False, status=200)

# posting comment of the product
@api_view(['POST'])
def post_comment(request, pk):
    data =request.data or {}
    product = Products.objects.filter(pk=pk)
    obj=product.first() 
    post= data.get('post')
    email = data.get('email')
    user= Users.objects.filter(gmail=email)
    user= user.first()
    comment = Comments.objects.create(product=obj, user=user, comment=post)
    comment.save()
    return Response({'comment':'comment posted'}, status=200)


# paginations and filters on products
@api_view(['GET'])
def products_page(request, pk):
    paginator = CustomPagination()
    if pk == 'allproducts':
         product_qs = Products.objects.all()  
    elif pk == 'females':
        product_qs = Products.objects.filter(gender='female')            
    elif pk =='males':
        product_qs = Products.objects.filter(gender='male')
    elif pk == 'kids':
        product_qs = Products.objects.filter(gender='kid')    
    else:
        return Response({}, status=404)
    paginated_qs= paginator.paginate_queryset(product_qs, request)
    serializer = ProductSerializer(paginated_qs, many=True)
    return paginator.get_paginated_response(serializer.data)

# creating user when logged in 
@api_view(['POST'])
def user_profile(request):
    data =request.data or {}
    username =data.get('name')
    email = data.get('email')
    image = data.get('image')
    user= Users.objects.filter(gmail= email)
    if user.exists():
        return Response({"user": "already existed"}, status=200)
    created_user=Users.objects.create(name=username, gmail=email, image=image)
    created_user.save()
    subscribe(email)
    return Response({"user": "user created"}, status=200)


# newsletter subscription
@api_view(['POST'])
def email_submittions(request):
    data= request.data or {}
    email= data.get('email')
    user= Users.objects.filter(gmail=email)
    if user.exists():
        return Response(f"{email} already existed", status=403)
    user.first()
    user= Users.objects.create(gmail=email)
    user.save()
    subscribe(email)
    return Response("You are Subscribed", status=200)


# getting user deta for form
@api_view(['POST'])
def getting_form(request):
    data= request.data or {}
    email= data.get('email')
    user= Users.objects.filter(gmail=email)
    if user is None:
        return Response({}, status=200)
    user= user.first()
    serializer = GetingUserSerializer(user, many=False)
    return Response(serializer.data, status=200)


# postting user data form form
@api_view(["POST"])
def posting_data(request):
    data= request.data or {}
    email= data.get('email')
    name= data.get('name')
    phone= data.get('phone')
    user= Users.objects.filter(gmail=email)
    if user.exists():
        user= user.first()
        user.name= name
        user.phone= phone
        user.complete= True
        user.save()
        print("save01")
        return Response("It has been Summited", status=200)
    user=Users.objects.create(name=name,phone=phone,gmail=email,complete=True)
    user.save()
    subscribe(email)
    return Response("It has been Summited", status=200)     



   
