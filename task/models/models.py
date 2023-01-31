from django.db import models


class Order_detail(models.Model):
    cart_value = models.IntegerField()
    delivery_distance = models.IntegerField()
    number_of_items = models.IntegerField()
    time = models.DateTimeField()

