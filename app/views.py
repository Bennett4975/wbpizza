from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.urls import reverse
from datetime import datetime, timedelta


def index(request):

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # retrieve customer id and save it to session
            username = form.cleaned_data.get("username")
            customer = get_object_or_404(Customer, username=username)
            request.session['id'] = customer.id
            return redirect(reverse('home'))
        else:
            return render(request, 'index.html', {'form': form})
    
    else:
        # ensures if a user logs out that all session details are cleared
        request.session.clear()
        form = SignupForm()
        return render(request, 'index.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            customer = get_object_or_404(Customer, username=username)
            request.session['id'] = customer.id
            return redirect(reverse('home'))
        else:
            return render(request, 'login.html', {'form' : form})
    
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def home(request):
    customerid = request.session.get("id")
    customer = get_object_or_404(Customer, id=customerid)
    orders = Order.objects.filter(customer=customer)
    return render(request, "home.html", {"customer" : customer, "orders":orders})


def pizza(request):
    if request.method == "POST":
        form = CreatePizzaForm(request.POST)
        if form.is_valid():
            form.save()
            pizza = Pizza.objects.all()
            pizza = pizza[len(pizza) - 1]
            request.session['pizzaid'] = pizza.id
            return redirect(reverse(order))
        else:
            return render(request, 'create_pizza.html', {'form':form})

    else:
        form = CreatePizzaForm()
        customerid = request.session.get("id")
        customer = get_object_or_404(Customer, id=customerid)
        return render(request, "create_pizza.html", {"customer" : customer, "form" : form})

def order(request):
    if request.method == "POST":
        form = OrderPizzaForm(request.POST)
        if form.is_valid():
            # save the form and retrieve the most recently saved order object
            form.save()
            order = Order.objects.all()
            order = order[len(order) - 1]
            request.session["orderid"] = order.id
            return redirect(reverse(confirmed))

        else:
            return render(request, 'order.html', {'form':form})
    
    else:
        form = OrderPizzaForm()
        return render(request, "order.html", {'form':form})
    
def confirmed(request):
    # retrieve all necessary objects
    customerid = request.session.get("id")
    customer = get_object_or_404(Customer, id=customerid) 
    pizzaid = request.session.get("pizzaid")
    pizza = get_object_or_404(Pizza, id=pizzaid)
    orderid = request.session.get("orderid")
    order = get_object_or_404(Order, id=orderid)

    # last setting up for the order, dont want it to be properly set up until customer can see order confirmed screen
    order.time = datetime.now() + timedelta(minutes=45)
    order.customer = customer
    order.pizza = pizza
    order.save()
    # link order details to customer to set as default
    customer.name = order.name
    customer.address = order.address
    customer.card_number = order.card_number
    customer.expiration_date = order.expiration_date
    customer.ccv = order.ccv
    customer.save()

    return render(request, "order_confirmed.html", {"pizza":pizza, "customer":customer, 'order':order})