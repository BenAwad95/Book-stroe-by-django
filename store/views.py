from django.shortcuts import render
from django.http import JsonResponse

from .models import *
from .utils import *

import json

def store(request):
    cookieName = 'cart'
    order = getOrder(request, cookieName)
    books = Product.objects.all()
    context = {
        'page_title': 'Home Page',
        'books':books,
        'order':order
    }
    return render(request,'store\home.html',context)


def cart(request):
    order = getOrder(request, 'cart')
    items = getItems(request, 'cart')
    context = {
        'page_title':'Cart',
        'order':order,
        'items':items,
    }
    return render(request,'store\cart.html',context)


def checkout(request):
    order = getOrder(request, 'cart')
    items = getItems(request, 'cart')
    context = {
        'page_title':'Cart',
        'order':order,
        'items':items
    }
    return render(request,'store\checkout.html',context)

def bookDetail(request,bookname):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complate = False)
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        order = {
            'get_total_cart':0,
            'get_items_cart':0,
            'complate':0
        }
        for productId in cart:
            try:#this is for products that may delete from the db and stile reminded in the car cookie
                product = Product.objects.get(pk = productId)
                order['get_items_cart'] += cart[productId]['quantity']
                order['get_total_cart'] += (cart[productId]['quantity'] * product.price)
            except:
                pass
    book = Product.objects.get(name=bookname)
    biggerText = False
    if len(book.brief) > 500:
        biggerText = True
    # print(len(book.brief))
    # print(biggerText)
    context = {
        'page_title':'Detail',
        'book':book,
        'order':order,
        'biggerText':biggerText
    }
    return render(request,'store\detail.html',context)

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
    if request.user.is_authenticated:
        customer  = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complate=False)
        shippingAddress.objects.create(order=order,country=shippingDetail['country'],city=shippingDetail['city'],street=shippingDetail['street'],zipCode=shippingDetail['zipCode'])
        order.complate = True
        order.save()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        name = data['userForm']['name']
        email = data['userForm']['email']
        # print(name,email)
        customer, created = Customer.objects.get_or_create(email=email)
        order = Order.objects.create(customer = customer, complate = False)
        for productId in cart:
            product = Product.objects.get(pk = productId)
            OrderItem.objects.create(order = order, product = product,
                quantity = cart[productId]['quantity']
            )
        shippingAddress.objects.create(
            order = order,
            country = shippingDetail['country'],
            city = shippingDetail['city'],
            street = shippingDetail['street'],
            zipCode = shippingDetail['zipCode'],
        )
        # print(order.orderitem_set.all())
    return JsonResponse('Payment has been successfully complete!\nThank you for shipping with us', safe= False)




def customerAccount(request,name):
    customer = Customer.objects.get(name=name)
    context = {
        'page_title':'Customer Account'
    }
    return render(request,'store/customerAccount.html',context)