from django.db import models

class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Sauce(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Cheese(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    id = models.IntegerField(primary_key=True)
    
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=1)
    Normal = "Normal"

    crust_choices = [
        ("Normal", "Normal"),
        ("Thick", "Thick"),
        ("Thin", "Thin"),
        ("Gluten Free", "Gluten Free"),
    ]

    crust = models.CharField(max_length =11, choices=crust_choices, default=Normal)

    sauce = models.ForeignKey(Sauce, on_delete=models.CASCADE, default=1)

    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE, default=1)

    # toppings:
    pepperoni = models.BooleanField(default=False)
    chicken = models.BooleanField(default=False)
    ham = models.BooleanField(default=False)
    pineapple = models.BooleanField(default=False)
    peppers = models.BooleanField(default=False)
    mushrooms = models.BooleanField(default=False)
    onions = models.BooleanField(default=False)

class Customer(models.Model):
    id=models.IntegerField(primary_key=True)
    # log in details
    username= models.CharField(max_length=15)
    password=models.CharField(max_length=20)
    password_again=models.CharField(max_length=20)
    # saved order details
    name=models.CharField(max_length=15)
    address=models.TextField()
    card_number=models.CharField(max_length=16)
    ccv=models.CharField(max_length=3)
    expiration_date=models.CharField(max_length=5)

class Order(models.Model):
    # order id
    id=models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=15)
    address=models.TextField()
    card_number=models.CharField(max_length=16)
    ccv=models.CharField(max_length=3)
    expiration_date=models.CharField(max_length=5)
    time=models.DateTimeField(null=True, blank=True)



