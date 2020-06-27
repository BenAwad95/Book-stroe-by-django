from django.shortcuts import render

def store(request):
    context = {
        'page_title': 'Home Page'
    }
    return render(request,'store\home.html',context)
