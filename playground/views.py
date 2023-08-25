from turtle import title
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from store.models import Product

def say_hello(request):
    queryset = Product.objects.all()
    return render(request, 'hello.html', { 'products': list(queryset)})
