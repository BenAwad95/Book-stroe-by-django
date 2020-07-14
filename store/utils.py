from .models import *
import json
def getCookieData(request, cookieName):
    try:
        cartData = json.loads(request.COOKIES[cookieName])
    except:
        return False
    return cartData


def getOrder(request, cookieName):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except:
            customer = Customer.objects.create(user = request.user, name = request.user.first_name, email = request.user.email)
        order, created = Order.objects.get_or_create(customer = customer, complate = False)
    else:
        order = {
            'get_total_cart':0,
            'get_items_cart':0,
            'complate':0
        }
        cartData = getCookieData(request, cookieName)
        if cartData:
            for prodcutId in cartData:
                product = Product.objects.get(id = prodcutId)
                order['get_items_cart'] += cartData[prodcutId]['quantity']
                order['get_total_cart'] += cartData[prodcutId]['quantity'] * product.price
        else:
            print("couldn't get product")

    return order


def getItems(request, cookieName):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except:
            customer = Customer.objects.create(user = request.user, name = request.user.first_name, email = request.user.email)
        order, created = Order.objects.get_or_create(customer = customer, complate = False)
        items = order.orderitem_set.all()
    else:
        cartData = getCookieData(request, cookieName)
        items = []
        for productId in cartData:
            try:
                product = Product.objects.get(id = productId)
                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,
                    },
                    'quantity': cartData[productId]['quantity'],
                    'get_total': (cartData[productId]['quantity'] * product.price)
                }
                items.append(item)
            except:
                print("there is error here at utils.py")
                pass
    return items
