from django.shortcuts import render, redirect, reverse

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.urls import reverse

from .forms import *
from .utils import *


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully')
            user = User.objects.get(username = request.POST.get('username'))
            customer = Customer.objects.create(user = user, name = request.POST.get('first_name'), email = request.POST.get('email'))
            order = Order.objects.create(customer = customer, complate = False)
            cartDate = json.loads(request.COOKIES['cart'])
            for productId in cartDate:
                product = Product.objects.get(id = productId)
                OrderItem.objects.create(order = order, product = product,
                quantity =(cartDate[productId]['quantity']) )
            return redirect(reverse("acounts:login"))
            
            # reverse('login')
            # return login(request)
    cookieName = 'cart'
    order = getOrder(request, cookieName)
    context = {
        'order':order,
        'form':form,
        'page_title':'log in',
    }

    return render(request,'acounts/register.html',context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect(reverse("store:store"))
        else:
            messages.error(request,'Username or password not vialed')
    cookieName = 'cart'            
    order = getOrder(request, cookieName)
    context = {
        'order': order,
        'page_title':'log in',
    }
    

    return render(request,'acounts/login.html',context)


def logoutUser(request):
    logout(request)
    messages.info(request, "You logout successfully")
    return redirect(reverse("acounts:login"))



