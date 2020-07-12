from django.shortcuts import render
from .models import *

from django.http import JsonResponse
import json

def store(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except:
            customer = Customer.objects.create(user = request.user, name = request.user.first_name, email = request.user.email)
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
    books = Product.objects.all()
    context = {
        'page_title': 'Home Page',
        'books':books,
        'order':order
    }
    return render(request,'store\home.html',context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complate = False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        order = {
            'get_total_cart':0,
            'get_items_cart':0,
        }
        items = []
        for productId in cart:
            try: 
                product = Product.objects.get(pk = productId)
                order['get_items_cart'] += cart[productId]['quantity']
                order['get_total_cart'] += (cart[productId]['quantity'] * product.price)
                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,
                    },
                    'quantity': cart[productId]['quantity'],
                    'get_total': (cart[productId]['quantity'] * product.price)
                }
                items.append(item)
                # print(item)
            except:
                pass
    # print(items)
    context = {
        'page_title':'Cart',
        'order':order,
        'items':items,
    }
    return render(request,'store\cart.html',context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complate = False)
        items = order.orderitem_set.all()
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
        items = []
        for productId in cart:
            try:
                product = Product.objects.get(pk = productId)
                order['get_items_cart'] += cart[productId]['quantity']
                order['get_total_cart'] += (cart[productId]['quantity'] * product.price)
                item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity': cart[productId]['quantity'],
                'get_total': (cart[productId]['quantity'] * product.price)
                }
                items.append(item)
            # print(item)
            except:
                pass
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