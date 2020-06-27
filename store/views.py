from django.shortcuts import render

def store(request):
    context = {
        'page_title': 'Home Page'
    }
    return render(request,'store\home.html',context)


def cart(request):
    context = {
        'page_title':'Cart'
    }
    return render(request,'store\cart.html',context)


def checkout(request):
    context = {
        'page-title':'checkout'
    }
    return render(request,'store\checkout.html',context)