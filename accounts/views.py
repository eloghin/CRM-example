from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import Customer, Product, Order
from accounts.forms import CustomerForm, OrderForm, ProductForm, UserSignupForm
from accounts.filters import OrderFilter


def welcome(request):
    return render(request, 'accounts/welcome.html')


@login_required(login_url='login')
def dashboard(request):
    customer_records = Customer.objects.all()
    order_records = Order.objects.all().order_by('-date_created')[:5]

    order_total = Order.objects.all().count()
    order_delivered = Order.objects.filter(status = 'Delivered').count()
    order_pending = Order.objects.filter(status = 'Pending').count()
    order_out_for_delivery = Order.objects.filter(status = 'Out for delivery').count()

    return render(request, 'accounts/dashboard.html',
            {'customer_records': customer_records,
             'order_records': order_records,
             'order_total': order_total,
             'order_delivered': order_delivered,
             'order_pending': order_pending,
             'order_out_for_delivery': order_out_for_delivery})


@login_required(login_url='login')
def products(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 10) # Show 10 products per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'accounts/products.html', {'page_obj': page_obj})


@login_required(login_url='login')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'accounts/product_form.html', {'form':form, 'header': 'Create new product:'})


@login_required(login_url='login')
def update_product(request, pk):
    product = Product.objects.get(id = pk)
    form = ProductForm(instance = product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance = product)
        if form.is_valid():
            form.save()
            return redirect('products') #redirect to products.html

    return render(request, 'accounts/product_form.html', {'form':form, 'header':'Update product:'})


@login_required(login_url='login')
def delete_product(request, pk):
    product = Product.objects.get(id = pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products')

    return render(request, 'accounts/delete_product.html', {'item': product})


@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    return render(request, 'accounts/customer.html',
            {'customer': customer,
            'orders': orders,
            'order_count': order_count,
            'myFilter': myFilter})


@login_required(login_url='login')
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/') #redirect to dashboard
    else:
        form = CustomerForm()
    return render(request, 'accounts/customer_form.html', {'form':form})


@login_required(login_url='login')
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    print(customer)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/') #redirect to dashboard
    else:
        formset = OrderFormSet()
    return render(request, 'accounts/order_formset.html', {'formset':formset, 'customer':customer})


@login_required(login_url='login')
def update_order(request, pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance = order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('/') #redirect to dashboard

    return render(request, 'accounts/order_form.html', {'form':form, 'header': 'Update Order:'})


@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id = pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete_order.html', {'item': order})


def create_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = UserSignupForm(data=request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created successfully for ' + user +'. You can login now.')
                return redirect('login')
            else:
                print(form.errors)
        else:
            form = UserSignupForm()

        return render(request, 'registration/create_user.html', {'form': form})
