from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="index"),
   path('home/', views.home, name="home"),
   path('login/', views.login, name="login"),
   path('home/order/pizza', views.pizza, name="pizza"),
   path('home/order/', views.order, name="order"),
   path('home/order/confirmed', views.confirmed, name="order_confirmed"),
  # path('home/order/confirmed', views.confirmed, name='confirmed')
]