from django.shortcuts import render

# Create your views here.
from store.serializers import ProductSerializer, CategorySerializer
from store.models import Product, Category


from rest_framework import generics
from rest_framework.permissions import AllowAny


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(status="published")
    permission_classes = (AllowAny,)
