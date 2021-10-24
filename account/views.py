from django.db.models.query import QuerySet
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
# from django.http import HttpResponse
from .forms import OrderForm, CreateUserForm, CustomerForm
from .models import *
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'account/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'account/login.html', context)


def logoutUser(request):

    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               'total_customers': total_customers, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'account/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'account/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'account/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def products(request):
    products = Product.objects.all()
    return render(request, 'account/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'account/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, id):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=id)
    formset = OrderFormSet(instance=customer, queryset=Order.objects.none())
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print("Printing POST: ",request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'account/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, id):

    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'account/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, id):

    order = Order.objects.get(id=id)

    if request.POST:
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'account/delete.html', context)
