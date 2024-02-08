from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    modelimages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Products
        fields = [
            "id",
            "name",
            "price",
            "old_price",
            "image",
            "modelimages",
            "measurement",
            "slug",
        ]

    def get_modelimages(self, obj):
        images = Crop_pictures.objects.filter(product=obj)
        return [image.Image_MAIN for image in images][0:3]


class ProductDetailsSerializer(serializers.ModelSerializer):
    crop_images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Products
        fields = [
            "id",
            "name",
            "price",
            "old_price",
            "image",
            "video",
            "description_span",
            "description",
            "crop_images",
            "Meta_Title",
            "Meta_description",
            "slug",
            "measurement",
        ]

    def get_crop_images(self, obj):
        images = Crop_pictures.objects.filter(product=obj)
        return [image.Image_MAIN for image in images]


class CommentsSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    checkedlast = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comments
        fields = ["comment", "user", "image", "checkedlast"]

    def get_user(self, obj):
        return obj.user.name

    def get_comment(self, obj):
        return obj.comment

    def get_image(self, obj):
        return obj.user.Image_MAIN

    def get_checkedlast(self, obj):
        return obj.checkedlast


class TestimonialsSerializer(serializers.Serializer):
    client_picture = serializers.SerializerMethodField(read_only=True)
    client_name = serializers.SerializerMethodField(read_only=True)
    client_comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Testimonials

        fields = ["client_comment", "client_picture", "client_name"]

    def get_client_picture(self, obj):
        return obj.client_picture_URL

    def get_client_name(self, obj):
        return obj.client_name

    def get_client_comment(self, obj):
        return obj.client_comment


class VideosSerializer(serializers.Serializer):
    video = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = videoPlayer

        fields = ["video"]

    def get_video(self, obj):
        return obj.Video_MAIN


class LikesSerializer(serializers.Serializer):
    likescount = serializers.SerializerMethodField(read_only=True)
    userliked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = Products
        fields = ["likescount", "userliked"]

    def get_likescount(self, obj):
        return obj.liked.count()

    def get_userliked(self, obj):
        user = obj.liked.filter(liked__gmail=self.gmail)
        user = user.first()
        if user:
            return True
        return False


class GetingUserSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField(read_only=True)
    gmail = serializers.SerializerMethodField(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)
    phone = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = Users
        fields = ["name", "gmail", "address", "phone"]

    def get_name(self, obj):
        return obj.name

    def get_gmail(self, obj):
        return obj.gmail

    def get_address(self, obj):
        return obj.address

    def get_phone(self, obj):
        return obj.phone


class GetingItemsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    subprice = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.SerializerMethodField(read_only=True)
    measurement = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = UserItemsActions
        fields = [
            "id",
            "name",
            "image",
            "quantity",
            "price",
            "subprice",
            "measurement",
        ]

    def get_id(self, obj):
        return obj.product.id

    def get_name(self, obj):
        return obj.product.name

    def get_image(self, obj):
        return obj.product.Image_MAIN

    def get_price(self, obj):
        return obj.product.price

    def get_subprice(self, obj):
        return obj.subprice

    def get_quantity(self, obj):
        return obj.quantity

    def get_measurement(self, obj):
        return obj.measurement


class GetingListSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    measurement = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = UserItemslists
        fields = [
            "id",
            "name",
            "image",
            "price",
            "measurement",
        ]

    def get_id(self, obj):
        return obj.product.id

    def get_name(self, obj):
        return obj.product.name

    def get_image(self, obj):
        return obj.product.Image_MAIN

    def get_price(self, obj):
        return obj.product.price

    def get_measurement(self, obj):
        return obj.measurement


class ProductListSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.SerializerMethodField(read_only=True)
    delivery = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    sub_price = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = ProductItems
        fields = [
            "id",
            "slug",
            "name",
            "quantity",
            "delivery",
            "price",
            "sub_price",
            "image",
            "created_at",
        ]

    def get_id(self, obj):
        return obj.product.id

    def get_slug(self, obj):
        return obj.product.slug

    def get_name(self, obj):
        return obj.product.name

    def get_quantity(self, obj):
        return obj.quantity

    def get_delivery(self, obj):
        return obj.processing

    def get_price(self, obj):
        return obj.product.price

    def get_sub_price(self, obj):
        return obj.total_value

    def get_image(self, obj):
        return obj.product.Image_MAIN

    def get_created_at(self, obj):
        return obj.created_at


class FreeGiftListSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.SerializerMethodField(read_only=True)
    delivery = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    sub_price = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = ProductItems
        fields = [
            "name",
            "quantity",
            "delivery",
            "price",
            "sub_price",
            "image",
            "created_at",
        ]

    def get_name(self, obj):
        return obj.freegift.name

    def get_quantity(self, obj):
        return obj.quantity

    def get_delivery(self, obj):
        return obj.processing

    def get_price(self, obj):
        return obj.freegift.price

    def get_sub_price(self, obj):
        return obj.freegift.price

    def get_image(self, obj):
        return obj.freegift.Image_URL

    def get_created_at(self, obj):
        return obj.created_at


class CouponStateGetSerializer(serializers.Serializer):
    state = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = CouponState
        fields = ["state"]

    def get_state(self, obj):
        return obj.state


class FreeGiftSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    naira_price = serializers.SerializerMethodField(read_only=True)
    price_to_pass = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = FreeGift
        fields = ["name", "image", "naira_price", "price_to_pass"]

    def get_name(self, obj):
        return obj.name

    def get_image(self, obj):
        return obj.Image_URL

    def get_naira_price(self, obj):
        return obj.price

    def get_price_to_pass(self, obj):
        return obj.price_to_pass


# admin getting products
class AdminProductSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    old_price = serializers.SerializerMethodField(read_only=True)
    vendor_price = serializers.SerializerMethodField(read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    description_span = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    hot = serializers.SerializerMethodField(read_only=True)
    special = serializers.SerializerMethodField(read_only=True)
    out_of_product = serializers.SerializerMethodField(read_only=True)
    Meta_Title = serializers.SerializerMethodField(read_only=True)
    Meta_description = serializers.SerializerMethodField(read_only=True)
    vendor_name = serializers.SerializerMethodField(read_only=True)
    Vendor_contact = serializers.SerializerMethodField(read_only=True)
    vendor_location = serializers.SerializerMethodField(read_only=True)
    measurement = serializers.SerializerMethodField(read_only=True)
    created_on = serializers.SerializerMethodField(read_only=True)
    updated_on = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = Products
        fields = [
            "id",
            "name",
            "image",
            "price",
            "old_price",
            "vendor_price",
            "liked",
            "description",
            "description_span",
            "type",
            "category",
            "hot",
            "special",
            "out_of_product",
            "Meta_Title",
            "Meta_description",
            "vendor_name",
            "Vendor_contact",
            "vendor_location",
            "measurement",
            "created_on",
            "updated_on",
        ]

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_image(self, obj):
        return obj.Image_MAIN

    def get_price(self, obj):
        return obj.price

    def get_old_price(self, obj):
        return obj.old_price

    def get_vendor_price(self, obj):
        return obj.vendor_price

    def get_liked(self, obj):
        return obj.liked.count()

    def get_description(self, obj):
        return obj.description

    def get_description_span(self, obj):
        return obj.description_span

    def get_type(self, obj):
        return obj.type

    def get_category(self, obj):
        return obj.category

    def get_hot(self, obj):
        return obj.hot

    def get_special(self, obj):
        return obj.special

    def get_out_of_product(self, obj):
        return obj.out_of_product

    def get_Meta_Title(self, obj):
        return obj.Meta_Title

    def get_Meta_description(self, obj):
        return obj.Meta_description

    def get_vendor_name(self, obj):
        return obj.vendor_name

    def get_Vendor_contact(self, obj):
        return obj.Vendor_contact

    def get_vendor_location(self, obj):
        return obj.vendor_location

    def get_measurement(self, obj):
        return obj.measurement

    def get_created_on(self, obj):
        return obj.created_on

    def get_updated_on(self, obj):
        return obj.updated_on


class AdminScificSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    old_price = serializers.SerializerMethodField(read_only=True)
    vendor_price = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    description_span = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    hot = serializers.SerializerMethodField(read_only=True)
    special = serializers.SerializerMethodField(read_only=True)
    out_of_product = serializers.SerializerMethodField(read_only=True)
    Meta_Title = serializers.SerializerMethodField(read_only=True)
    Meta_description = serializers.SerializerMethodField(read_only=True)
    vendor_name = serializers.SerializerMethodField(read_only=True)
    vendor_image = serializers.SerializerMethodField(read_only=True)
    Vendor_contact = serializers.SerializerMethodField(read_only=True)
    vendor_location = serializers.SerializerMethodField(read_only=True)
    video = serializers.SerializerMethodField(read_only=True)
    measurement = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = Products
        fields = [
            "id",
            "name",
            "image",
            "price",
            "old_price",
            "vendor_price",
            "images",
            "description",
            "description_span",
            "type",
            "category",
            "hot",
            "special",
            "out_of_product",
            "Meta_Title",
            "Meta_description",
            "vendor_name",
            "Vendor_contact",
            "vendor_location",
            "vendor_image",
            "video" "measurement",
        ]

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_image(self, obj):
        return obj.Image_MAIN

    def get_price(self, obj):
        return obj.price

    def get_old_price(self, obj):
        return obj.old_price

    def get_vendor_price(self, obj):
        return obj.vendor_price

    def get_description(self, obj):
        return obj.description

    def get_description_span(self, obj):
        return obj.description_span

    def get_type(self, obj):
        return obj.type

    def get_category(self, obj):
        return obj.category

    def get_hot(self, obj):
        return obj.hot

    def get_special(self, obj):
        return obj.special

    def get_out_of_product(self, obj):
        return obj.out_of_product

    def get_Meta_Title(self, obj):
        return obj.Meta_Title

    def get_Meta_description(self, obj):
        return obj.Meta_description

    def get_vendor_name(self, obj):
        return obj.vendor_name

    def get_vendor_image(self, obj):
        return obj.Image_URL

    def get_Vendor_contact(self, obj):
        return obj.Vendor_contact

    def get_vendor_location(self, obj):
        return obj.vendor_location

    def get_video(self, obj):
        return obj.Video_MAIN

    def get_measurement(self, obj):
        return obj.measurement

    def get_images(self, obj):
        images = Crop_pictures.objects.filter(product=obj)
        return [image.Image_MAIN for image in images]


# admin getting Freegift
class AdminFreeGiftSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    price_to_pass = serializers.SerializerMethodField(read_only=True)
    vendor_name = serializers.SerializerMethodField(read_only=True)
    vendor_image = serializers.SerializerMethodField(read_only=True)
    Vendor_contact = serializers.SerializerMethodField(read_only=True)
    vendor_location = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = FreeGift
        fields = [
            "id",
            "name",
            "image",
            "price",
            "price_to_pass",
            "vendor_name",
            "vendor_image",
            "Vendor_contact",
            "vendor_location",
            "created_at",
            "updated_at",
        ]

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_image(self, obj):
        return obj.Image_URL

    def get_price(self, obj):
        return obj.price

    def get_price_to_pass(self, obj):
        return obj.price_to_pass

    def get_vendor_name(self, obj):
        return obj.vendor_name

    def get_vendor_image(self, obj):
        return obj.Vendor_Image_URL

    def get_Vendor_contact(self, obj):
        return obj.Vendor_contact

    def get_vendor_location(self, obj):
        return obj.vendor_location

    def get_created_at(self, obj):
        return obj.created_at

    def get_updated_at(self, obj):
        return obj.updated_at


class AdminUserClosedSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    location = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)
    funnel_complete = serializers.SerializerMethodField(read_only=True)
    total_money = serializers.SerializerMethodField(read_only=True)
    shipping_call = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = UserClosed
        fields = [
            "id",
            "name",
            "image",
            "phone_number",
            "email",
            "total_price",
            "location",
            "created_at",
            "updated_at",
            "funnel_complete",
            "total_money",
            "shipping_call",
        ]

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.user.name

    def get_image(self, obj):
        return obj.user.Image_MAIN

    def get_phone_number(self, obj):
        return obj.user.phone

    def get_email(self, obj):
        return obj.user.gmail

    def get_total_price(self, obj):
        return obj.all_total

    def get_location(self, obj):
        return obj.user.address

    def get_created_at(self, obj):
        return obj.created_at

    def get_updated_at(self, obj):
        return obj.updated_at

    def get_funnel_complete(self, obj):
        return obj.complete

    def get_total_money(self, obj):
        return obj.user.total_money

    def get_shipping_call(self, obj):
        return obj.shipping_call


class AdminGetProductsClientSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.SerializerMethodField(read_only=True)
    processing = serializers.SerializerMethodField(read_only=True)
    total_value = serializers.SerializerMethodField(read_only=True)
    measurement = serializers.SerializerMethodField(read_only=True)
    vendor_name = serializers.SerializerMethodField(read_only=True)
    Vendor_contact = serializers.SerializerMethodField(read_only=True)
    vendor_location = serializers.SerializerMethodField(read_only=True)
    schedule_date = serializers.SerializerMethodField(read_only=True)
    discussion = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    vendor_image = serializers.SerializerMethodField(read_only=True)
    vendor_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = ProductItems
        fields = [
            "id",
            "image",
            "vendor_image",
            "name",
            "price",
            "quantity",
            "processing",
            "total_value",
            "measurement",
            "vendor_name",
            "vendor_price",
            "Vendor_contact",
            "vendor_location",
            "schedule_date",
            "discussion",
            "created_at",
            "updated_at",
        ]

    def get_id(self, obj):
        return obj.id

    def get_image(self, obj):
        return obj.product.Image_MAIN

    def get_vendor_image(self, obj):
        return obj.product.Image_URL

    def get_name(self, obj):
        return obj.product.name

    def get_price(self, obj):
        return obj.product.price

    def get_quantity(self, obj):
        return obj.quantity

    def get_processing(self, obj):
        return obj.processing

    def get_total_value(self, obj):
        return obj.total_value

    def get_measurement(self, obj):
        return obj.product.measurement

    def get_vendor_price(self, obj):
        return obj.product.vendor_price

    def get_vendor_name(self, obj):
        return obj.product.vendor_name

    def get_Vendor_contact(self, obj):
        return obj.product.Vendor_contact

    def get_vendor_location(self, obj):
        return obj.product.vendor_location

    def get_schedule_date(self, obj):
        return obj.schedule_date

    def get_discussion(self, obj):
        return obj.discussion

    def get_created_at(self, obj):
        return obj.created_at

    def get_updated_at(self, obj):
        return obj.updated_at


class AdminGetFreeClientSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.SerializerMethodField(read_only=True)
    processing = serializers.SerializerMethodField(read_only=True)
    total_value = serializers.SerializerMethodField(read_only=True)
    measurement = serializers.SerializerMethodField(read_only=True)
    vendor_name = serializers.SerializerMethodField(read_only=True)
    Vendor_contact = serializers.SerializerMethodField(read_only=True)
    vendor_location = serializers.SerializerMethodField(read_only=True)
    schedule_date = serializers.SerializerMethodField(read_only=True)
    discussion = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    vendor_image = serializers.SerializerMethodField(read_only=True)
    vendor_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = ProductItems
        fields = [
            "id",
            "image",
            "vendor_image",
            "name",
            "price",
            "quantity",
            "processing",
            "total_value",
            "measurement",
            "vendor_name",
            "vendor_price",
            "Vendor_contact",
            "vendor_location",
            "schedule_date",
            "discussion",
            "created_at",
            "updated_at",
        ]

    def get_id(self, obj):
        return obj.id

    def get_image(self, obj):
        return obj.freegift.Image_URL

    def get_vendor_image(self, obj):
        return obj.freegift.Vendor_Image_URL

    def get_name(self, obj):
        return obj.freegift.name

    def get_price(self, obj):
        return None

    def get_quantity(self, obj):
        return obj.quantity

    def get_processing(self, obj):
        return obj.processing

    def get_total_value(self, obj):
        return obj.total_value

    def get_measurement(self, obj):
        return None

    def get_vendor_price(self, obj):
        return obj.freegift.price

    def get_schedule_date(self, obj):
        return None

    def get_discussion(self, obj):
        return None

    def get_vendor_name(self, obj):
        return obj.freegift.vendor_name

    def get_Vendor_contact(self, obj):
        return obj.freegift.Vendor_contact

    def get_vendor_location(self, obj):
        return obj.freegift.vendor_location

    def get_created_at(self, obj):
        return obj.created_at

    def get_updated_at(self, obj):
        return obj.updated_at


class AdminGetAllClientsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    phone = serializers.SerializerMethodField(read_only=True)
    gmail = serializers.SerializerMethodField(read_only=True)
    schedule_date = serializers.SerializerMethodField(read_only=True)
    discussion = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = Users
        fields = [
            "id",
            "name",
            "phone",
            "gmail",
            "schedule_date",
            "discussion",
            "created_at",
            "updated_at",
        ]

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_phone(self, obj):
        return obj.phone

    def get_gmail(self, obj):
        return obj.gmail

    def get_schedule_date(self, obj):
        return obj.schedule_date

    def get_discussion(self, obj):
        return obj.discussion

    def get_created_at(self, obj):
        return obj.created_at

    def get_updated_at(self, obj):
        return obj.updated_at


class AdminSeeTestimonialsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    client_name = serializers.SerializerMethodField(read_only=True)
    client_comment = serializers.SerializerMethodField(read_only=True)
    client_picture = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = Testimonials
        fields = ["id", "client_name", "client_comment", "client_picture", "created_at"]

    def get_id(self, obj):
        return obj.id

    def get_client_name(self, obj):
        return obj.client_name

    def get_client_comment(self, obj):
        return obj.client_comment

    def get_client_picture(self, obj):
        return obj.client_picture_URL

    def get_created_at(self, obj):
        return obj.created_at


class AdminSeeCouponsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    coupon_name = serializers.SerializerMethodField(read_only=True)
    owner_name = serializers.SerializerMethodField(read_only=True)
    owner_phone_number = serializers.SerializerMethodField(read_only=True)
    owner_email = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        models = Coupons
        fields = [
            "id",
            "coupon_name",
            "owner_name",
            "owner_phone_number",
            "owner_email",
            "created_at",
            "updated_at",
        ]

    def get_id(self, obj):
        return obj.id

    def get_coupon_name(self, obj):
        return obj.coupon_name

    def get_owner_name(self, obj):
        return obj.owner_name

    def get_owner_phone_number(self, obj):
        return obj.owner_phone_number

    def get_owner_email(self, obj):
        return obj.owner_email

    def get_created_at(self, obj):
        return obj.created_at

    def get_updated_at(self, obj):
        return obj.updated_at
