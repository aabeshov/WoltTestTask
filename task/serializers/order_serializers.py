from rest_framework import serializers
from task.models import Order_detail


class orderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order_detail
        fields = (
            'cart_value',
            'delivery_distance',
            'number_of_items',
            'time',
        )
