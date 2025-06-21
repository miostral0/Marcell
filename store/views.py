from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

import json

from .models import *

# Store view
def store(request):
    products = Product.objects.all()[:8]
    context = {'products':products}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total_price = sum(item.get_total for item in items)
        total_items = sum(item.quantity for item in items)
    else:
        items = []
        total_price = 0
        total_items = 0

    context = {
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
    }
    return render(request, 'store/cart.html', context)



def remove_item(request, item_id):
    if request.user.is_authenticated:
        item = OrderItem.objects.get(id=item_id, order__customer=request.user.customer)
        item.delete()
    return redirect('cart') 

# CheckOut view
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total_price = sum(item.get_total for item in items)
        total_items = sum(item.quantity for item in items)
    else:
        items = []
        total_price = 0
        total_items = 0

    context = {
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
    }
    return render(request, 'store/checkout.html', context)

# LogIn view
def logIn(request):
    context = {}
    return render(request, 'store/logIn.html', context)

# SignUp view
def signUp(request):
    context = {}
    return render(request, 'store/SignUp.html', context)

# Shop view
def shop(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/Shop.html', context)

# WhatsNew view
def New(request):
    new_products = Product.objects.all().order_by('-date_added')[:4]
    best_for_you_products = Product.objects.all().order_by('-date_added')[4:8]
    context = {
        'new_products': new_products,
        'best_for_you_products': best_for_you_products,
    }
    return render(request, 'store/new.html', context)


def submit_order(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']
        

        order = Order.objects.create(
            email=email,
            name=name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            total_price=request.POST.get('total_price')
        )
        return redirect('order_confirmation')
    return redirect('cart')

def update_cart_item(request):
    data = json.loads(request.body)
    item_id = data['itemId']
    quantity = int(data['quantity'])

    item = OrderItem.objects.get(id=item_id)
    item.quantity = quantity
    item.save()

    return JsonResponse({'message': 'Quantity updated'})

def remove_item(request, item_id):
    if request.method == 'POST':
        item = OrderItem.objects.get(id=item_id)
        item.delete()
        return redirect('cart')
    
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({
        'message': f"{product.name} quantity updated to {orderItem.quantity if orderItem.quantity > 0 else 0}",
        'cart_items': order.get_cart_items
    })


def update_cart_quantity(request):
    data = json.loads(request.body)
    item_id = data['item_id']
    quantity = int(data['quantity'])

    item = OrderItem.objects.get(id=item_id)
    item.quantity = quantity
    item.save()

    order = item.order
    total_price = order.get_cart_total
    total_items = order.get_cart_items

    return JsonResponse({
        'message': 'Quantity updated',
        'total_price': total_price,
        'total_items': total_items
    })

def logIn(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')  # redirect to your main store page or dashboard
        else:
            message = "Invalid username or password."

    context = {'message': message}
    return render(request, 'store/logIn.html', context)