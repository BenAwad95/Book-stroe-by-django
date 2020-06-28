from django.shortcuts import render
from .models import *

from django.http import JsonResponse
import json

def store(request):
    order, created = Order.objects.get_or_create(customer = request.user.customer, complate = False)
    books = Product.objects.all()
    context = {
        'page_title': 'Home Page',
        'books':books,
        'order':order
    }
    return render(request,'store\home.html',context)


def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complate=False)
    context = {
        'page_title':'Cart',
        'order':order
    }
    return render(request,'store\cart.html',context)


def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complate=False)
    context = {
        'page-title':'checkout',
        'order':order
    }
    return render(request,'store\checkout.html',context)


def updateItem(request):
    # print('it is working')
    data = json.loads(request.body)
    # print(data['action'])
    action = data['action']
    product = Product.objects.get(id = int(data['productId']))
    customer  = request.user.customer
    order, created = Order.objects.get_or_create(customer = customer, complate=False)
    orderitem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse('I faced a big problem here', safe = False)


def processOrder(request):
    data = json.loads(request.body)
    shippingDetail = data['shippingDetail']
    customer  = request.user.customer
    order, created = Order.objects.get_or_create(customer = customer, complate=False)
    shippingAddress.objects.create(order=order,country=shippingDetail['country'],city=shippingDetail['city'],street=shippingDetail['street'],zipCode=shippingDetail['zipCode'])
    order.complate = True
    order.save()
    return JsonResponse('Payment has been successfully complete!\nThank you for shipping with us', safe= False)