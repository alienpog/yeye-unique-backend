from django.urls import path
from .views import getting_all_customers,testimonial_page, product_page,productlikes,getting_form,posting_data,post_comment,email_submittions,postlike,products_page,likescount,user_profile, comments, mostliked, testimonials,videoplayer,products_details

urlpatterns = [
    path('product/<slug:pk>/', products_details),
    path('testimonial/', testimonial_page),
    path('customers/', getting_all_customers),
    path('comments/<int:pk>/', comments),
    path('mostliked/', mostliked),
    path("loginuser/", user_profile),
    path('testimonials/', testimonials),
    path('videoplay/', videoplayer),
    path('productlikes/<int:pk>/', productlikes),
    path('postlike/<int:pk>/', postlike),
    path('postcomment/<int:pk>/', post_comment),
    path('likescount/<int:pk>/',likescount),
    path('newsletter/', email_submittions),
    path('gettingform/', getting_form),
    path('postingform/', posting_data),
    path('', product_page),
    path ('<str:pk>/', products_page),
]
