from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("customer_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    name = models.CharField( max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    degital = models.BooleanField(default=False)
    image = models.ImageField(null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

    
    

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
    complate = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_cart(self):
        return sum(item.get_total for item in self.orderitem_set.all())
    
    def get_items_cart(self):
        return sum(item.quantity for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default = 0)
    
    def __str__(self):
        return str(self.order.id)
    
    @property
    def get_total(self):
        total = self.quantity * self.product.price
        # print(total)
        return total

    
    