from django.shortcuts import render
from pan.tasks import update_stock_info
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView(APIView):
    def get(self, request, format=None):
        update_stock_info()
        return Response({"message": "success"})
