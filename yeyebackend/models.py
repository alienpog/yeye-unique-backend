from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


# video
class videoPlayer(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    video = models.FileField(blank=True, null=True)

    @property
    def Video_MAIN(self):
        if self.video:
            Url = self.video.url
        else:
            Url = ""
        return Url

    def __str__(self):
        return self.title


# Users
class Users(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    gmail = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    follow_up = models.BooleanField(default=False)
    schedule_date = models.CharField(max_length=150, null=True, blank=True)
    discussion = models.TextField(null=True, blank=True)
    total_money = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=True, blank=True)

    @property
    def Image_MAIN(self):
        if self.image:
            Url = self.image.url
        else:
            Url = ""
        return Url

    def __str__(self):
        return self.gmail


# Products
class Products(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    old_price = models.FloatField(blank=True, null=True)
    liked = models.ManyToManyField(Users, blank=True)
    description = models.TextField(blank=True, null=True)
    description_span = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50)
    category = models.TextField(blank=True, null=True)
    hot = models.BooleanField(default=False)
    special = models.BooleanField(default=False)
    out_of_product = models.BooleanField(default=False)
    size = models.CharField(max_length=50, blank=True, null=True)
    Meta_Title = models.CharField(max_length=250, blank=True, null=True)
    Meta_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    vendor_name = models.CharField(max_length=200, blank=True, null=True)
    vendor_image = models.FileField(blank=True, null=True)
    Vendor_contact = models.IntegerField(blank=True, null=True)
    vendor_price = models.IntegerField(blank=True, null=True)
    vendor_location = models.TextField(blank=True, null=True)
    video = models.FileField(blank=True, null=True)
    measurement = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def Image_URL(self):
        if self.vendor_image:
            Url = self.vendor_image.url
        else:
            Url = ""
        return Url

    @property
    def Image_MAIN(self):
        if self.image:
            Url = self.image.url
        else:
            Url = ""
        return Url

    @property
    def Video_MAIN(self):
        if self.video:
            Url = self.video.url
        else:
            Url = ""
        return Url

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        to_assign = slugify(self.name)

        if Products.objects.filter(slug=to_assign).exists():
            to_assign = to_assign + str(Products.objects.all().count())

        self.slug = to_assign

        super().save(*args, **kwargs)


# Crop_pictures
class Crop_pictures(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField()

    @property
    def Image_MAIN(self):
        if self.image:
            Url = self.image.url
        else:
            Url = ""
        return Url

    def __str__(self):
        return self.product.name


# Comments
class Comments(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    checkedlast = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


# Testimonials
class Testimonials(models.Model):
    client_name = models.CharField(max_length=200, null=True, blank=True)
    client_comment = models.TextField(null=True, blank=True)
    client_picture = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def client_picture_URL(self):
        if self.client_picture:
            Url = self.client_picture.url
        else:
            Url = ""
        return Url

    def __str__(self):
        return self.client_name


# User Product Items
class ProductItems(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True
    )
    freegift = models.ForeignKey(
        "FreeGift", on_delete=models.CASCADE, null=True, blank=True
    )
    userclosed = models.ForeignKey(
        "UserClosed", on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    schedule_date = models.CharField(max_length=150, null=True, blank=True)
    discussion = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    processing = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_value(self):
        if self.product:
            data = self.product.price * self.quantity
        else:
            data = None
        return data

    def __str__(self):
        if self.product:
            data = self.product.name + " " + self.user.name
        else:
            data = "fregift" + " " + self.user.name
        return data


# User FreeGift
class FreeGift(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    price_to_pass = models.FloatField(blank=True, null=True)
    vendor_name = models.CharField(max_length=200, blank=True, null=True)
    vendor_image = models.FileField(blank=True, null=True)
    Vendor_contact = models.IntegerField(blank=True, null=True)
    vendor_location = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def Image_URL(self):
        if self.image:
            Url = self.image.url
        else:
            Url = ""
        return Url

    @property
    def Vendor_Image_URL(self):
        if self.vendor_image:
            Url = self.vendor_image.url
        else:
            Url = ""
        return Url

    def __str__(self):
        if self.name is not None:
            return self.name
        return "Unknown"


# UserClosed
class UserClosed(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    all_total = models.FloatField(blank=True, null=True)
    shipping_call = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    new_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            self.user.name
            + "  "
            + self.user.phone
            + "  "
            + self.user.gmail
            + "  "
            + str(self.created_at)
        )


# Cartitems
class UserItemsActions(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True
    )
    subprice = models.FloatField(blank=True, null=True)
    measurement = models.BooleanField(default=False)

    def __str__(self):
        return self.user.gmail + self.product.name


# Cartlists
class UserItemslists(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True
    )
    measurement = models.BooleanField(default=False)

    def __str__(self):
        return self.user.gmail + self.product.name


# coupon data
class Coupons(models.Model):
    coupon_name = models.CharField(max_length=150, null=True, blank=True)
    owner_name = models.CharField(max_length=150, null=True, blank=True)
    owner_phone_number = models.IntegerField(null=True, blank=True)
    owner_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coupon_name


# checking if the user used the coupon
class UserCoupons(models.Model):
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coupon.coupon_name + " " + self.user.gmail


# coupon state update
class CouponState(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.user.gmail


# price state update
class PriceState(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    state = models.IntegerField(null=True, blank=True)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.gmail


# Total amount spent still on process
# Total amount spent still on process
class UserCartPrice(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    state = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name + " " + str(self.state) + " " + str(self.created_at)


# Total amount spent still on process
# Total amount spent still on process
