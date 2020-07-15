from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import *
from .utils import *
from .forms import *

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
    cookieName = 'cart'
    order = getOrder(request, cookieName)
    items = getItems(request, cookieName)
    context = {
        'page_title':'Cart',
        'order':order,
        'items':items,
    }
    return render(request,'store\cart.html',context)

def checkout(request):
    cookieName = 'cart'
    order = getOrder(request, cookieName)
    items = getItems(request, cookieName)
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
        customer, created = Customer.objects.get_or_create(name = name, email=email)
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
        order.complate = True
        # print(order.orderitem_set.all())
    return JsonResponse('Payment has been successfully complete!\nThank you for shipping with us', safe= False)

def registerCheckout(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username = request.POST.get('username'))
            login(request,authenticate(username=request.POST.get('username'),password=request.POST.get('password1')))
            customer = Customer.objects.create(user = user, name = request.POST.get('first_name'), email = request.POST.get('email'))
            order = Order.objects.create(customer = customer, complate = False)
            cartDate = json.loads(request.COOKIES['cart'])
            for productId in cartDate:
                product = Product.objects.get(id = productId)
                OrderItem.objects.create(order = order, product = product,
                quantity =(cartDate[productId]['quantity']) )
            # print(cartDate[productId]['quantity'])
            # messages.success(request, 'Your account has been created successfully')
            return redirect(reverse("store:checkout"))
    context = {
        'form':form,
        'page_title':'Sing Up',
    }

    return render(request,'store/checkoutRegister.html',context)

def loginCheckout(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            customer = user.customer
            order, created = Order.objects.get_or_create(customer = customer, complate = False)
            products = list(orderitem.product for orderitem in order.orderitem_set.all())
            cartDate = json.loads(request.COOKIES['cart'])
            for productId in cartDate:
                product = Product.objects.get(id = productId)
                if product in products:
                    for item in order.orderitem_set.all():
                        if item.product == product:
                            item.quantity += (cartDate[productId]['quantity'])
                            item.save()
                else:
                    OrderItem.objects.create(order = order, product = product,
                quantity =(cartDate[productId]['quantity']) )
            return redirect(reverse("store:checkout"))
        else:
            messages.error(request,'Username or password not vialed')

    context = {
        'page_title':'log in',
    }


    return render(request,'store/loginCheckout.html',context)

def customerAccount(request,name):
    customer = Customer.objects.get(name=name)
    context = {
        'page_title':'Customer Account'
    }
    return render(request,'store/customerAccount.html',context)