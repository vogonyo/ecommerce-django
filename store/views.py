from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import datetime
import json


# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'delivery': False
        }
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems
    }
    return render(request, 'store/store.html', context)

def home(request):
    return render(request, 'store/home.html')
    
def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

def sutures(request):
    products = Product.objects.filter(category='SU')
    print(products)
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)


def labware(request):
    products = Product.objects.filter(category='LA')
    print(products)
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)


def equipment(request):
    products = Product.objects.filter(category='EQ')
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)


def instruments(request):
    products = Product.objects.filter(category='IN')
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)

def culture(request):
    products = Product.objects.filter(category='CU')
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)

def media(request):
    products = Product.objects.filter(category='ME')
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'delivery': False
        }
        cartItems = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
     }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'delivery': False
        }
        cartItems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
     }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer;
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.delivery == True:
            DeliveryAddress.objects.create(
                customer = customer,
                order=order,
                address=data['delivery']['address'],
                city=data['delivery']['city'],
                phone=data['delivery']['phone']
            )
    else:
        print('User is not logged in...')
    return JsonResponse('Payment Complete!', safe=False)