
import json
from math import ceil
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from task.serializers.order_serializers import orderDetailSerializer
from rest_framework.response import Response
from task.models import Order_detail
from datetime import datetime


# Class Based View
class calc_delivery_fee(APIView):
    # Using GET method, can be cached, less safe
    def get(self, request):
        serializer = orderDetailSerializer(data=request.query_params)
        if serializer.is_valid():
            total_fee = 0
            Delivery = Order_detail(**serializer.data)

            if Delivery.cart_value > 10000:
                return Response({"delivery_fee": 0}, status=status.HTTP_200_OK)
            # Cart Value Condition
            if Delivery.cart_value < 1000:
                total_fee += 10 - (Delivery.cart_value/100)
                print(total_fee)
            # Delivery Distance Conditions
            if Delivery.delivery_distance <= 500:
                total_fee += 1
            else:
                total_fee += (ceil(Delivery.delivery_distance / 500))
            # Total items Conditions
            if Delivery.number_of_items >= 5:
                total_fee += (Delivery.number_of_items - 4) * 50
                if Delivery.number_of_items > 12:
                    total_fee += 1.2

            # Rush Hour
            time_now = datetime.fromisoformat(Delivery.time[:-1])
            if datetime.weekday(time_now) == 5:
                if 13 <= time_now.hour <= 19:
                    total_fee *= 1.2

            # Final Condition
            if total_fee > 1500:
                total_fee = 1500

            return Response({"delivery_fee": (int(total_fee * 100))}, status=status.HTTP_200_OK)

        # Error return
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Using POST method, can't be cached, more safe
    def post(self, request):
        serializer = orderDetailSerializer(data=request.query_params)
        if serializer.is_valid():
            total_fee = 0
            Delivery = Order_detail(**serializer.data)
            if Delivery.cart_value > 10000:
                return Response({"delivery_fee": 0}, status=status.HTTP_200_OK)
            if Delivery.cart_value < 1000:
                total_fee += 10 - (Delivery.cart_value/100)
                print(total_fee)
            if Delivery.delivery_distance <= 500:
                total_fee += 1
            else:
                total_fee += (ceil(Delivery.delivery_distance / 500))
            if Delivery.number_of_items >= 5:
                total_fee += (Delivery.number_of_items - 4) * 50
                if Delivery.number_of_items > 12:
                    total_fee += 1.2
            time_now = datetime.fromisoformat(Delivery.time[:-1])
            if datetime.weekday(time_now) == 5:
                if 13 <= time_now.hour <= 19:
                    total_fee *= 1.2
            if total_fee > 1500:
                total_fee = 1500
            return Response({"delivery_fee": (int(total_fee * 100))}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

