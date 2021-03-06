from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    SUTURES = 'SU'
    LABWARE = 'LA'
    EQUIPMENT = 'EQ'
    INSTRUMENTS = 'IN'
    CULTURE = 'CU'
    MEDIA = 'ME'

    CATEGORY_CHOICES = [
        (SUTURES, 'Sutures'),
        (LABWARE, 'Labware'),
        (EQUIPMENT, 'Equipment'),
        (INSTRUMENTS, 'Instruments'),
        (CULTURE, 'Culture'),
        (MEDIA, 'Media')
    ]

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    measurement = models.CharField(max_length=250, null=True, blank=True)
    unit = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=LABWARE)
    sold_out = models.BooleanField(default = False)
    digital = models.BooleanField(default = False, null = True , blank = False)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default = False)
    transaction_id = models.CharField(max_length=100, null= True)

    def __str__(self):
        return str(self.id)

    @property
    def delivery(self):
        delivery = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                delivery = True
        return delivery

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total
    
    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class DeliveryAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=250, null=False)
    city  = models.CharField(max_length=250, null= False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address