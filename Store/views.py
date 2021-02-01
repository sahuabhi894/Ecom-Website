from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime


from .models import *
from .utils import cookieCart,cartData,guestOrder


# after delete



# from django.contrib.auth.forms import UserCreationForm

# from django.contrib.auth import authenticate, login, logout

# from django.contrib import messages

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import Group

# from .forms import  CreateUserForm
# from .decorators import unauthenticated_user, allowed_users, admin_only

# yha tk


#  this part for user auth.................................
# @unauthenticated_user
# def registerPage(request):

# 	form = CreateUserForm()
# 	if request.method == 'POST':
# 		form = CreateUserForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			username = form.cleaned_data.get('username')

# 			group = Group.objects.get(name='customer')
# 			user.groups.add(group)

# 			messages.success(request, 'Account was created for ' + username)

# 			return redirect('login')
		

# 	context = {'form':form}
# 	return render(request, 'Store/register.html', context)

# @unauthenticated_user
# def loginPage(request):

# 	if request.method == 'POST':
# 		username = request.POST.get('username')
# 		password =request.POST.get('password')

# 		user = authenticate(request, username=username, password=password)

# 		if user is not None:
# 			login(request, user)
# 			return redirect('store')
# 		else:
# 			messages.info(request, 'Username OR password is incorrect')

# 	context = {}
# 	return render(request, 'Store/login.html', context)

# def logoutUser(request):
# 	logout(request)
# 	return redirect('login')

# .............................................................................................................................................................................

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def main(request):
#     home = addver.objects.all()
#     return render(request, 'Store/main.html', {'home':home})

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def store(request):
    data = cartData(request)
    cartItems =data['cartItems']



    products = Product.objects.all()
    context ={'products': products , 'cartItems':cartItems}
    return render(request, 'Store/store.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def cart(request):
    data = cartData(request)
    cartItems =data['cartItems']
    order = data['order']
    items = data['items']

       

    context ={'items':items , 'order':order , 'cartItems':cartItems}
    return render(request, 'Store/cart.html', context)



# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def checkout(request):
    
    data = cartData(request)
    cartItems =data['cartItems']
    order = data['order']
    items = data['items']

    context ={'items':items , 'order':order , 'cartItems':cartItems}
    return render(request, 'Store/checkout.html', context)





# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        

    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete() 



    return JsonResponse('Item was added', safe=False)


# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)




    else:
        customer,order = guestOrder(request,data)
       

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
         order.complete = True
    order.save()


    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address =data['shipping']['address'],
            city =data['shipping']['city'],
            state =data['shipping']['state'],
            zipcode =data['shipping']['zipcode'],

        )




    return JsonResponse('Payment Vomplete!', safe=False)