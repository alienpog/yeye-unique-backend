from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from .models import *
# Create your views here.


@api_view(['GET'])
def products_page(request):
    person = Products.objects.all()
    serializer = ProductSerializer(person, many=True)
    return Response(serializer.data)