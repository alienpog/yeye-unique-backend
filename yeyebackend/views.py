from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ProductSerializer,
    TestimonialsSerializer,
    CommentsSerializer,
    VideosSerializer,
    ProductDetailsSerializer,
    GetingUserSerializer,
    GetingItemsSerializer,
    GetingListSerializer,
    ProductListSerializer,
    CouponStateGetSerializer,
    FreeGiftSerializer,
    FreeGiftListSerializer,
    AdminProductSerializer,
    AdminScificSerializer,
    AdminFreeGiftSerializer,
    AdminUserClosedSerializer,
    AdminGetProductsClientSerializer,
    AdminGetFreeClientSerializer,
    AdminGetAllClientsSerializer,
    AdminSeeTestimonialsSerializer,
    AdminSeeCouponsSerializer,
)
from .models import *
from django.db.models import Count, Sum
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import operator
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.http import Http404


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
    mailchimp.set_config(
        {
            "api_key": api_key,
            "server": server,
        }
    )

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
    page_size = 1  # Number of items to display per page
    page_size_query_param = (
        "page_size"  # URL query parameter for overriding the page size
    )


# puttin product in the database
def product_page(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                name = request.POST["name"]
                priceold = request.POST["priceold"]
                pricenew = request.POST["pricenew"]
                description = request.POST["description"]
                description_span = request.POST["description_span"]
                Image = request.FILES["Image"]
                type = request.POST["gender"]
                Crop_Images = request.FILES.getlist("Crop_Images")
                hot = request.POST.get("hot", False) == "on"
                special = request.POST.get("special", False) == "on"
                measurement = request.POST.get("measurement", False) == "on"
                Meta_Title = request.POST["Meta_Title"]
                Meta_description = request.POST["Meta_description"]

                # print("name>>>",name,
                #      "priceold>>>>>",priceold,
                #      "pricenew>>>",pricenew,
                #      "Currency>>>>",Currency,
                #      "zero_price>>>",zero_price,
                #      "description>>>",description,
                #      "description_span>>>>",description_span,
                #      "Image>>>>>",Image,
                #      "gender>>>>>",gender,
                #      "Crop_Images>>>",Crop_Images,
                #      "color>>>>",color,
                #      "catalog>>>>>",catalog,
                #      "materials_type>>>>",materials_type,
                #      "hot>>>>",hot,
                #      "unique>>>",unique,
                #      "Meta_Title",Meta_Title,
                #      "Meta_description",Meta_description)
                product = Products.objects.create(
                    name=name,
                    image=Image,
                    price=pricenew,
                    old_price=priceold,
                    description=description,
                    measurement=measurement,
                    description_span=description_span,
                    type=type,
                    hot=hot,
                    special=special,
                    Meta_Title=Meta_Title,
                    Meta_description=Meta_description,
                )
                product.save()
                for image in Crop_Images:
                    crop_picture = Crop_pictures.objects.create(
                        image=image, product=product
                    )
                    crop_picture.save()
                    print("uploaded to the database")
            except:
                print("not uploaded to the database")
        return render(request, "index.html")
    return redirect("https://www.google.com")


# putting testimonal in the database
def testimonial_page(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                name = request.POST.get("name")
                comment = request.POST.get("comment")
                Image = request.FILES["Image"]
                testimonial = Testimonials.objects.create(
                    client_name=name, client_comment=comment, client_picture=Image
                )
                testimonial.save()
            except:
                print("not uploaded")
        return render(request, "testimonial.html")
    return redirect("https://www.google.com")


def getting_all_customers(request):
    if request.user.is_authenticated:
        clients = Users.objects.all().order_by("-updated_at")
        return render(request, "customers.html", {"clients": clients})
    return redirect("https://www.google.com")


# specific data of the product
@api_view(["GET"])
def products_details(request, pk):
    person = Products.objects.filter(slug=pk)
    if not person.exists():
        return Response({}, status=404)
    person = person.first()
    serializer = ProductDetailsSerializer(person, many=False)
    return Response(serializer.data)


# geting  all comments of a product
@api_view(["GET"])
def comments(request, pk):
    comments = Comments.objects.filter(product=pk).order_by("-checkedlast")
    if not comments.exists():
        return Response([], status=200)
    serializer = CommentsSerializer(comments, many=True)
    return Response(serializer.data)


# collecting dataquary products
@api_view(["GET"])
def dataquary(request, pk):
    if pk == "mostliked":
        products = Products.objects.annotate(like_count=Count("liked")).order_by(
            "-like_count"
        )
    elif pk == "womendesign":
        products = Products.objects.filter(type="female")
    elif pk == "wristwatches":
        products = Products.objects.filter(type="watches")
    elif pk == "mendesign":
        products = Products.objects.filter(type="male")
    elif pk == "kidsdesign":
        products = Products.objects.filter(type="kid")
    elif pk == "jewelleries":
        products = Products.objects.filter(type="jewelry")
    else:
        products = Products.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# all testimony products
@api_view(["GET"])
def testimonials(request):
    clients = Testimonials.objects.all()
    serializer = TestimonialsSerializer(clients, many=True)
    return Response(serializer.data)


# video player
@api_view(["GET"])
def videoplayer(request):
    videos = videoPlayer.objects.all().exclude(title="thank you video")
    serializer = VideosSerializer(videos, many=True)
    return Response(serializer.data)


# video player for thank you video
@api_view(["GET"])
def thank_you_video(request):
    videos = videoPlayer.objects.get(title="thank you video")
    serializer = VideosSerializer(videos, many=False)
    return Response(serializer.data)


# counting likes
@api_view(["GET"])
def likescount(request, pk):
    product = Products.objects.filter(id=pk)
    obj = product.first()
    number = obj.liked.count()
    return Response(number, status=200)


# when user clicks on a like and unlike button
@api_view(["POST"])
def postlike(request, pk):
    data = request.data or {}
    product = Products.objects.filter(id=pk)
    obj = product.first()
    email = data.get("email")
    user = Users.objects.filter(gmail=email)
    if user is None:
        return Response(False, status=200)
    user = user.first()
    action = data.get("action")
    if action == "like":
        obj.liked.add(user)
        return Response(True, status=200)
    if action == "unlike":
        obj.liked.remove(user)
        return Response(False, status=200)


# checking if the user liked or not liked on first load
@api_view(["POST"])
def productlikes(request, pk):
    data = request.data or {}
    product = Products.objects.filter(id=pk)
    obj = product.first()
    email = data.get("email")
    user = Users.objects.filter(gmail=email)
    # b4: if user is None also don't forget {"likes": False}:
    if not user.exists():
        return Response(False, status=200)
    if user.first() in obj.liked.all():
        return Response(True, status=200)
    return Response(False, status=200)


# posting comment of the product
@api_view(["POST"])
def post_comment(request, pk):
    data = request.data or {}
    product = Products.objects.filter(pk=pk)
    obj = product.first()
    post = data.get("post")
    email = data.get("email")
    user = Users.objects.filter(gmail=email)
    user = user.first()
    comment = Comments.objects.create(product=obj, user=user, comment=post)
    comment.save()
    return Response({"comment": "comment posted"}, status=200)


# paginations and filters on products
@api_view(["GET"])
def products_page(request, pk):
    paginator = CustomPagination()
    if pk == "none":
        slugs = Products.objects.all()
        serializer = ProductDetailsSerializer(slugs, many=True)
        return Response(serializer.data)
    elif pk == "allproducts":
        product_qs = Products.objects.all().order_by("-created_on")
    elif pk == "female":
        product_qs = Products.objects.filter(type="female")
    elif pk == "male":
        product_qs = Products.objects.filter(type="male")
    elif pk == "kids":
        product_qs = Products.objects.filter(type="kid")
    elif pk == "men-shoes":
        product_qs = Products.objects.filter(type="men-shoe")
    elif pk == "men-caps":
        product_qs = Products.objects.filter(type="men-cap")
    elif pk == "Jewelleries":
        product_qs = Products.objects.filter(type="jewelry")
    elif pk == "wristwatches":
        product_qs = Products.objects.filter(type="watches")
    elif pk == "women-bags":
        product_qs = Products.objects.filter(type="women-bag")
    else:
        product_qs = Products.objects.filter(
            Q(name__icontains=pk) | Q(type__icontains=pk)
        )
    paginated_qs = paginator.paginate_queryset(product_qs, request)
    serializer = ProductSerializer(paginated_qs, many=True)
    return paginator.get_paginated_response(serializer.data)


# creating user when logged in
@api_view(["POST"])
def user_profile(request):
    data = request.data or {}
    username = data.get("name")
    email = data.get("email")
    image = data.get("image")
    user = Users.objects.filter(gmail=email)
    if user.exists():
        return Response({"user": "already existed"}, status=200)
    created_user = Users.objects.create(name=username, gmail=email, image=image)
    created_user.save()
    subscribe(email)
    return Response({"user": "user created"}, status=200)


# newsletter subscription
@api_view(["POST"])
def email_submittions(request):
    data = request.data or {}
    email = data.get("email")
    user = Users.objects.filter(gmail=email)
    if user.exists():
        return Response(f"{email} already existed", status=403)
    user.first()
    user = Users.objects.create(gmail=email)
    user.save()
    subscribe(email)
    return Response("You are Subscribed", status=200)


# getting user deta for form
@api_view(["POST"])
def getting_form(request):
    data = request.data or {}
    email = data.get("email")
    user = Users.objects.filter(gmail=email)
    if user is None:
        return Response({}, status=200)
    user = user.first()
    serializer = GetingUserSerializer(user, many=False)
    return Response(serializer.data, status=200)


# postting user data form form
@api_view(["POST"])
def posting_data(request):
    data = request.data or {}
    email = data.get("email")
    name = data.get("name")
    phone = data.get("phone")
    user = Users.objects.filter(gmail=email)
    if user.exists():
        user = user.first()
        user.name = name
        user.phone = phone
        user.follow_up = True
        user.save()
        return Response("It has been Summited", status=200)
    user = Users.objects.create(name=name, phone=phone, gmail=email, follow_up=True)
    user.save()
    subscribe(email)
    return Response("It has been Summited", status=200)


# postting user data form form
@api_view(["POST"])
def posting_address(request):
    data = request.data or {}
    email = data.get("email")
    name = data.get("name")
    phone = data.get("phone")
    address = data.get("address")
    user = Users.objects.filter(gmail=email)
    if user.exists():
        user = user.first()
        user.name = name
        user.phone = phone or None
        user.address = address or None
        user.save()
        return Response("It has been Summited", status=200)
    return Response({}, status=200)


# getting cart items for user from data
@api_view(["POST"])
def getting_items(request):
    data = request.data or {}
    email = data.get("email")
    user = Users.objects.filter(gmail=email)
    user = user.first()
    dataitems = UserItemsActions.objects.filter(user=user)
    serializer = GetingItemsSerializer(dataitems, many=True)
    return Response(serializer.data, status=200)


# postting user cart to database
@api_view(["POST"])
def posting_items(request):
    data = request.data or {}
    cart = data.get("cart")
    gmail = data.get("session")
    user = Users.objects.filter(gmail=gmail)
    if not user.exists():
        return Response({}, status=404)
    user = user.first()
    try:
        userdata = UserItemsActions.objects.filter(user=user)
        userdata.delete()
    except:
        pass
    if cart != None:
        for item in cart:
            id = item["id"]
            quantity = item["quantity"]
            subprice = item["subprice"]
            measurement = item["measurement"]
            product = Products.objects.filter(id=id)
            if not product.exists():
                return Response({}, status=404)
            product = product.first()
            dataitems = UserItemsActions.objects.create(
                user=user,
                quantity=quantity,
                product=product,
                subprice=subprice,
                measurement=measurement,
            )
            dataitems.save()
    return Response({}, status=200)


# getting user wishlist data from database
@api_view(["POST"])
def getting_list(request):
    data = request.data or {}
    email = data.get("email")
    user = Users.objects.filter(gmail=email)
    user = user.first()
    dataitems = UserItemslists.objects.filter(user=user)
    serializer = GetingListSerializer(dataitems, many=True)
    return Response(serializer.data, status=200)


# postting user wishlist data to database
@api_view(["POST"])
def posting_list(request):
    data = request.data or {}
    list = data.get("list")
    gmail = data.get("session")
    user = Users.objects.filter(gmail=gmail)
    if not user.exists():
        return Response({}, status=404)
    user = user.first()
    try:
        userdata = UserItemslists.objects.filter(user=user)
        userdata.delete()
    except:
        pass
    if list != None:
        for item in list:
            id = item["id"]
            measurement = item["measurement"]
            product = Products.objects.filter(id=id)
            if not product.exists():
                return Response({}, status=404)
            product = product.first()
            dataitems = UserItemslists.objects.create(
                user=user,
                product=product,
                measurement=measurement,
            )
            dataitems.save()
    return Response({}, status=200)


# getting user amount from data
@api_view(["POST"])
def user_amount(request):
    data = request.data or {}
    gmail = data.get("email")
    user = Users.objects.filter(gmail=gmail)
    if not user.exists():
        return Response({}, status=404)
    user02 = user.first()
    number = user02.total_money
    return Response(number, status=200)


# posting user data and closing them also
@api_view(["POST"])
def close_user(request):
    data = request.data or {}
    email = data.get("email")
    total = data.get("total")
    items = data.get("items")

    try:
        user = Users.objects.get(gmail=email)
    except Users.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    usertotal = user.total_money + total

    try:
        pending_price, _ = UserCartPrice.objects.get_or_create(user=user)
        pending_price.state = total
        pending_price.save()
    except Exception as e:
        # Handle exceptions if necessary
        pass

    shipping_call = False
    try:
        shipping = PriceState.objects.get(user=user)
        shipping02 = shipping.shipping_state
        if shipping02 == "Our agents will contact you for the Shipping Fee":
            shipping_call = True
    except PriceState.DoesNotExist:
        pass

    # Create a closed user record
    closed_user = UserClosed.objects.create(
        user=user, all_total=total, complete=True, shipping_call=shipping_call
    )

    for item in items:
        id = item["id"]
        quantity = item["quantity"]
        try:
            product = Products.objects.get(id=id)
        except Products.DoesNotExist:
            return Response({"message": f"Product with ID {id} not found"}, status=404)

        item = ProductItems.objects.create(
            product=product, quantity=quantity, user=user, userclosed=closed_user
        )

    try:
        data = PriceState.objects.get(user=user)
        data.delete()
    except PriceState.DoesNotExist:
        pass

    # user_total_money = user.total_money

    # try:
    #     product = (
    #         FreeGift.objects.filter(price_to_pass__lt=usertotal)
    #         .order_by("-price_to_pass")
    #         .first()
    #     )

    #     if product:
    #         data = ProductItems.objects.filter(freegift=product, user=user)
    #         if not data.exists():
    #             item = ProductItems.objects.create(
    #                 freegift=product, quantity=1, user=user, userclosed=closed_user
    #             )
    #             item.save()
    #             return Response({"message": "Item created successfully"}, status=201)
    #         else:
    #             return Response({"data": "Data already exists"}, status=200)

    try:
        product = (
            FreeGift.objects.filter(price_to_pass__lt=usertotal)
            .order_by("-price_to_pass")
            .first()
        )
        print("see Product", product)
        if product:
            data = ProductItems.objects.filter(freegift=product, user=user)
            if not data.exists():
                item = ProductItems.objects.create(
                    freegift=product, quantity=1, user=user, userclosed=closed_user
                )
                item.save()
                return Response({"message": "Item created successfully"}, status=201)
            else:
                return Response({"data": "Data already exists"}, status=200)

    except FreeGift.DoesNotExist:
        print("message", "No eligible FreeGift found")
        return Response({"message": "No eligible FreeGift found"}, status=404)

    return Response({}, status=200)


# getting user data product
@api_view(["POST"])
def getting_user_products(request):
    data = request.data or {}
    email = data.get("email")

    # Retrieve the user or return a 404 response if not found
    try:
        user = Users.objects.get(gmail=email)
    except Users.DoesNotExist:
        raise Http404("User not found")

    # Filter products and free gifts associated with this user and exclude those without a product or free gift
    product_list = ProductItems.objects.filter(
        user=user, product__isnull=False
    ).order_by("-created_at")

    product_list02 = ProductItems.objects.filter(
        user=user, freegift__isnull=False
    ).order_by("-created_at")

    # Serialize the data using the serializers you provided
    data01 = ProductListSerializer(product_list, many=True)
    data02 = FreeGiftListSerializer(product_list02, many=True)

    # Combine the data from products and free gifts
    combined_data = data02.data + data01.data

    # Sort the combined data by 'created_at' in descending order
    combined_data = sorted(combined_data, key=lambda x: x["created_at"], reverse=True)

    return Response(combined_data, status=200)


@api_view(["POST"])
def checking_user_coupon(request):
    data = request.data or {}
    gmail = data.get("gmail")
    coupon = data.get("coupon")

    with transaction.atomic():
        try:
            user = Users.objects.get(gmail=gmail)
        except Users.DoesNotExist:
            return Response("You are not a user", status=400)

        try:
            user_coupon = Coupons.objects.get(coupon_name=coupon)
        except Coupons.DoesNotExist:
            return Response("Invalid coupon", status=400)

        coupon_number = UserCoupons.objects.filter(coupon=user_coupon).count()
        if coupon_number > 100:
            return Response("Coupon expired", status=400)

        coupon_used = UserCoupons.objects.filter(coupon=user_coupon, user=user)
        if not coupon_used.exists():
            UserCoupons.objects.create(coupon=user_coupon, user=user)
            return Response("Coupon accepted", status=200)
        else:
            return Response("Coupon already used by you", status=400)


# user coupon set when accepted
@api_view(["POST"])
def user_coupon_set(request):
    data = request.data or {}
    email = data.get("email")
    coupon_state = data.get("coupon")

    try:
        user = Users.objects.get(gmail=email)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    try:
        deleting = CouponState.objects.filter(user=user)
        deleting.delete()
    except ObjectDoesNotExist:
        pass

    if coupon_state == "Coupon accepted":
        coupon = CouponState.objects.create(user=user, state=coupon_state)
        coupon.save()
    return Response({}, status=404)


@api_view(["POST"])
def user_coupon_get(request):
    data = request.data or {}
    gmail = data.get("email")
    user = Users.objects.filter(gmail=gmail)
    if not user.exists():
        return Response({}, status=404)
    user02 = user.first()
    coupon = CouponState.objects.filter(user=user02)
    if not coupon.exists():
        return Response({}, status=404)
    coupon02 = coupon.first()
    serializer = CouponStateGetSerializer(coupon02, many=False)
    return Response(serializer.data, status=200)


@api_view(["POST"])
def user_pricestate(request):
    data = request.data or {}
    email = data.get("email")
    price_state = data.get("price")
    shipping_state = data.get("shipping")

    try:
        user = Users.objects.get(gmail=email)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    try:
        price_obj = PriceState.objects.filter(user=user)
        price_obj.delete()
    except ObjectDoesNotExist:
        pass
    created = PriceState.objects.create(
        user=user, shipping_state=shipping_state, state=price_state
    )
    created.save()
    return Response({}, status=200)


# getting the price state
@api_view(["POST"])
def user_priceget(request):
    data = request.data or {}
    gmail = data.get("email")
    user = Users.objects.filter(gmail=gmail)
    if not user.exists():
        return Response({}, status=404)
    user02 = user.first()
    try:
        price = PriceState.objects.get(user=user02)
        number = price.state
        return Response({"number": number}, status=200)
    except:
        pass


# getting the user free gift
@api_view(["POST"])
def free_gift(request):
    data = request.data or {}
    gmail = data.get("email")

    try:
        user = Users.objects.get(gmail=gmail)
        user_total_money = user.total_money  # Fix the variable name to user_total_money
    except Users.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    try:
        product = (
            FreeGift.objects.filter(price_to_pass__gt=user_total_money)
            .order_by("price_to_pass")
            .first()
        )
    except FreeGift.DoesNotExist:
        product = None

    if product:
        serializer = FreeGiftSerializer(product, many=False)
        return Response(serializer.data, status=200)
    else:
        return Response({"message": "No eligible free gift found"}, status=404)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def amdinseeproduct(request):
    product = Products.objects.all().order_by("-created_on")
    serializer = AdminProductSerializer(product, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admin_search(request, pk):
    query = pk.lower()
    querydata = Products.objects.filter(
        Q(name__icontains=query)
        | Q(type__icontains=query)
        | Q(vendor_name__icontains=query)
        | Q(category__icontains=query)
    ).order_by("-created_on")
    if not querydata.exists():
        querydata = Products.objects.all().order_by("-created_on")
    serializer = AdminProductSerializer(querydata, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def amdinqueryproduct(request, pk):
    try:
        product = Products.objects.get(pk=pk)
    except:
        return Response(404, status=404)
    serializer = AdminScificSerializer(product, many=False)
    return Response(serializer.data, status=200)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def adminproductsubmit(request):
    data = request.data or {}
    id = data.get("id")
    try:
        data_obj = Products.objects.get(id=id)
        data_obj.name = data.get("name")
        data_obj.price = data.get("price")
        data_obj.old_price = data.get("old_price")
        data_obj.vendor_price = data.get("vendor_price")
        data_obj.description = data.get("description")
        data_obj.description_span = data.get("description_span")
        data_obj.type = data.get("type")
        data_obj.category = data.get("category")
        data_obj.hot = True if data.get("hot") == "true" else False
        data_obj.special = True if data.get("special") == "true" else False
        data_obj.out_of_product = (
            True if data.get("out_of_product") == "true" else False
        )
        data_obj.Meta_Title = data.get("Meta_Title")
        data_obj.Meta_description = data.get("Meta_description")
        data_obj.vendor_name = data.get("vendor_name")
        data_obj.Vendor_contact = data.get("Vendor_contact")
        data_obj.vendor_location = data.get("vendor_location")
        data_obj.measurement = True if data.get("measurement") == "true" else False
        data_obj.save()
        return Response("Data Updated", status=200)
    except:
        product = Products.objects.create(
            name=data.get("name"),
            image=data.get("image"),
            price=data.get("price"),
            old_price=data.get("old_price"),
            vendor_price=data.get("vendor_price"),
            description=data.get("description"),
            description_span=data.get("description_span"),
            type=data.get("type"),
            category=data.get("category"),
            hot=True if data.get("hot") == "true" else False,
            special=True if data.get("special") == "true" else False,
            out_of_product=True if data.get("out_of_product") == "true" else False,
            Meta_Title=data.get("Meta_Title"),
            Meta_description=data.get("Meta_description"),
            vendor_name=data.get("vendor_name"),
            vendor_image=data.get("vendor_image"),
            Vendor_contact=data.get("Vendor_contact"),
            vendor_location=data.get("vendor_location"),
            video=data.get("video"),
            measurement=True if data.get("measurement") == "true" else False,
        )
        product.save()
        images = request.FILES.getlist("images[]")
        for image in images:
            img = Crop_pictures.objects.create(product=product, image=image)
            img.save()
        return Response("Data Created", status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def adminseefree(request):
    product = FreeGift.objects.all().order_by("-created_at")
    serializer = AdminFreeGiftSerializer(product, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def adminfreesearch(request, pk):
    query = pk.lower()
    querydata = FreeGift.objects.filter(
        Q(name__icontains=query) | Q(vendor_name__icontains=query)
    ).order_by("-created_at")
    if not querydata.exists():
        querydata = FreeGift.objects.all().order_by("-created_at")
    serializer = AdminFreeGiftSerializer(querydata, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def adminqueryfreeproduct(request, pk):
    try:
        product = FreeGift.objects.get(pk=pk)
    except:
        return Response(404, status=404)
    serializer = AdminFreeGiftSerializer(product, many=False)
    return Response(serializer.data, status=200)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def adminfreegiftsubmit(request):
    data = request.data or {}
    id = data.get("id")
    try:
        data_obj = FreeGift.objects.get(id=id)
        data_obj.name = data.get("name")
        data_obj.price = data.get("price")
        data_obj.price_to_pass = data.get("price_to_pass")
        data_obj.vendor_name = data.get("vendor_name")
        data_obj.Vendor_contact = data.get("Vendor_contact")
        data_obj.vendor_location = data.get("vendor_location")
        data_obj.save()
        return Response("Data Updated", status=200)
    except:
        product = FreeGift.objects.create(
            name=data.get("name"),
            image=data.get("image"),
            price=data.get("price"),
            price_to_pass=data.get("price_to_pass"),
            vendor_name=data.get("vendor_name"),
            vendor_image=data.get("vendor_image"),
            Vendor_contact=data.get("Vendor_contact"),
            vendor_location=data.get("vendor_location"),
        )
        product.save()
        return Response("Data Created", status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admindeletefree(request, pk):
    try:
        product = FreeGift.objects.get(pk=pk)
        product.delete()
    except:
        pass
    return Response("Product Deleted", status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admindeleteproduct(request, pk):
    try:
        product = Products.objects.get(pk=pk)
        product.delete()
    except:
        pass
    return Response("Product Deleted", status=200)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def adminsummitpricing(request):
    data = request.data or {}
    productsname = data.get("productsname")
    name = productsname.lower()
    addprice = data.get("addprice")
    products = Products.objects.filter(
        Q(name__icontains=name) | Q(category__icontains=name)
    )
    if not products.exists():
        Response({}, status=404)
    for product in products:
        product.price += int(addprice)
        product.save()
        return Response({}, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def adminseeclosedcustomers(request):
    clients = UserClosed.objects.all().order_by("-created_at")
    serializer = AdminUserClosedSerializer(clients, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def adminsearchclose(request, pk):
    query = pk.lower()
    querydata = UserClosed.objects.filter(
        Q(user__name__icontains=query) | Q(user__gmail__icontains=query)
    ).order_by("-created_at")
    if not querydata.exists():
        querydata = UserClosed.objects.all().order_by("-created_at")
    serializer = AdminUserClosedSerializer(querydata, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def adminqueryclientdetails(request, pk):
    try:
        client = UserClosed.objects.get(pk=pk)
    except:
        return Response("No Data", status=404)
    serializer = AdminUserClosedSerializer(client, many=False)
    return Response(serializer.data, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admingetclientproducts(request, pk):
    try:
        # Retrieve the client or return a 404 response if not found
        client = UserClosed.objects.get(pk=pk)
    except UserClosed.DoesNotExist:
        raise Http404("Client does not exist")

    # Filter products that are associated with this client and exclude those without a product
    products01 = ProductItems.objects.filter(
        userclosed=client, product__isnull=False
    ).order_by("-created_at")

    # Filter free gifts that are associated with this client and exclude those without a free gift
    products02 = ProductItems.objects.filter(
        userclosed=client, freegift__isnull=False
    ).order_by("-created_at")

    # Serialize the data using the serializers you provided
    data01 = AdminGetProductsClientSerializer(products01, many=True)
    data02 = AdminGetFreeClientSerializer(products02, many=True)

    # Combine the data from products and free gifts
    combined_data = data02.data + data01.data

    # Sort the combined data by 'created_at' in descending order
    combined_data = sorted(combined_data, key=lambda x: x["created_at"], reverse=True)

    return Response(combined_data, status=200)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def adminupdateclientproduct(request):
    data = request.data or {}
    id = data.get("id")
    clientdate = data.get("clientdate")
    clientprocess = data.get("clientprocess")
    clientdiscussion = data.get("clientdiscussion")
    print(clientdate, clientprocess, clientdiscussion)
    try:
        product = ProductItems.objects.get(pk=id)
    except:
        return Response("Product not found", status=404)
    product.processing = clientprocess
    product.schedule_date = clientdate
    product.discussion = clientdiscussion
    product.save()
    return Response("Product updated", status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admindeletefreegift(request, pk):
    try:
        product = ProductItems.objects.get(pk=pk)
    except:
        return Response("Product not found", status=404)
    product.delete()
    return Response("Product deleted", status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admingettotalprocessing(request, pk):
    try:
        user = UserClosed.objects.get(pk=pk)
    except UserClosed.DoesNotExist:
        return Response("User not found", status=404)

    user_products = ProductItems.objects.filter(userclosed=user)

    if not user_products.exists():
        return Response("Products not found", status=404)

    processing_statuses = [product.processing for product in user_products]

    if all(status == "done" for status in processing_statuses):
        if user.paid == False:
            user_money = user.all_total
            user.user.total_money += user_money
            user.user.save()
            user.paid = True
            user.save()
        return Response("done", status=200)
    elif all(status == "cancel" for status in processing_statuses):
        return Response("done", status=200)
    else:
        return Response("pending", status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admingetnavnumbers(request):
    product_count = Products.objects.aggregate(count=Count("id"))["count"]
    user_count = Users.objects.aggregate(count=Count("id"))["count"]
    free_gift_count = FreeGift.objects.aggregate(count=Count("id"))["count"]
    revenue_number = (
        Users.objects.aggregate(total_revenue=Sum("total_money"))["total_revenue"] or 0
    )
    return Response(
        {
            "product_count": product_count,
            "free_gift_count": free_gift_count,
            "user_count": user_count,
            "revenue_number": revenue_number,
        },
        status=200,
    )


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admingetallcontactclients(request):
    contact = Users.objects.filter(follow_up=True).order_by("-updated_at")
    if not contact.exists():
        return Response("NO Data", status=404)
    serializer = AdminGetAllClientsSerializer(contact, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def admin_update_contact_client(request):
    data = request.data or {}
    id = data.get("id")
    client_date = data.get("clientdate")
    client_process = data.get("clientprocess")
    client_discussion = data.get("clientdiscussion")

    try:
        client = Users.objects.get(id=id)
    except Users.DoesNotExist:
        return Response("Client not found", status=404)

    if client_process == "done":
        client.follow_up = False
        client.schedule_date = ""
        client.discussion = ""
        client.save()
        return Response("Client status updated", status=200)

    client.schedule_date = client_date
    client.discussion = client_discussion
    client.save()

    return Response("Client information updated", status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admin_see_testimonials(request):
    testimonials = Testimonials.objects.all().order_by("-created_at")
    serializer = AdminSeeTestimonialsSerializer(testimonials, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def admin_testimonial_submit(request):
    data = request.data or {}
    clientname = data.get("clientname")
    clienttestimonial = data.get("clienttestimonial")
    clientimage = data.get("clientimage")
    client = Testimonials.objects.create(
        client_name=clientname,
        client_comment=clienttestimonial,
        client_picture=clientimage,
    )
    client.save()
    return Response("Success", status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admin_see_coupons(request):
    coupons = Coupons.objects.all().order_by("-created_at")
    serializer = AdminSeeCouponsSerializer(coupons, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admin_query_count(request, pk):
    try:
        coupon_state = Coupons.objects.get(pk=pk)
    except Coupons.DoesNotExist:
        return Response(404, status=404)
    try:
        coupon_number = UserCoupons.objects.filter(coupon=coupon_state)
    except UserCoupons.DoesNotExist:
        return Response("no data found", status=404)
    number = coupon_number.count()
    return Response(number, status=200)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def admin_search_coupons(request, pk):
    query = pk.lower()
    querydata = Coupons.objects.filter(
        Q(coupon_name__icontains=query)
        | Q(owner_name__icontains=query)
        | Q(owner_email__icontains=query)
        | Q(owner_phone_number__icontains=query)
    ).order_by("-created_at")
    if not querydata.exists():
        querydata = Coupons.objects.all().order_by("-created_at")
    serializer = AdminSeeCouponsSerializer(querydata, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def admin_coupon_submit(request):
    data = request.data or {}
    couponname = data.get("couponname")
    couponowner = data.get("couponowner")
    ownerphonenumber = data.get("ownerphonenumber")
    owneremail = data.get("owneremail")
    coupon = Coupons.objects.create(
        coupon_name=couponname,
        owner_name=couponowner,
        owner_phone_number=ownerphonenumber,
        owner_email=owneremail,
    )
    coupon.save()
    return Response("Success", status=200)


@api_view(["POST"])
def admin_login_status(request):
    data = request.data or {}
    username = data.get("username")
    password = data.get("password")
    try:
        user = Users.objects.get(name=username, password=password)
    except Users.DoesNotExist:
        return Response("Error user not found", status=404)
    user_status = user.admin
    return Response(user_status, status=200)


@api_view(["GET"])
def query_search_products(request, pk):
    search = pk.lower()
    query_search_products = Products.objects.filter(Q(name__icontains=search))
    if not query_search_products.exists():
        return Response({}, status=404)
    serializer = ProductSerializer(query_search_products, many=True)
    return Response(serializer.data, status=200)
