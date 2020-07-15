from django.urls import path
from .views import *

# for image url
# --------
from django.conf import settings
from django.conf.urls.static import static
# --------

app_name = 'store'
urlpatterns = [
    path('', store, name="store"),
    path('cart/', cart, name="cart"),
    path('checkout/',checkout,name="checkout"),
    path('view/<str:bookname>/',bookDetail,name='bookDetail'),
    path('update-cart/', updateItem),
    path('process-order/', processOrder),
    path('customer/<str:name>/',customerAccount, name= 'customerAccount'),
    path('register-checkout',registerCheckout, name='registerCheckout'),
    path('login-checkout',loginCheckout, name='loginCheckout'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
