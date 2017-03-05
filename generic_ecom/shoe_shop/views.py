from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _

from django.views import View

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import models
from lib_common import views as LibCommonViews
from serializers import InventorySerializer, InventoryOrderSerializer


class RestInventoryList(APIView):

    def get(self, request, format=None):
        inventory = models.Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)


class RestInventoryOrder(APIView):

    # todo:mal: this function can be refactored later
    def post(self, request, format=None):
        """ Current user will place order"""
        inventory_id = request.data.get('inventory_id', None)

        user_id = None
        if hasattr(request, 'user'):
            user_id = request.user.id

        if inventory_id is not None and user_id is not None:
            try:
                inventory_item = models.Inventory.objects.get(pk=inventory_id)
            except models.Inventory.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                user = models.ExtendedUser.objects.get(pk=user_id)
            except models.ExtendedUser.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                new_data = {}
                new_data['inventory'] = inventory_item
                new_data['customer'] = user
                new_order = models.InventoryOrder(**new_data)
                new_order.save()

                return Response(InventoryOrderSerializer(new_order).data)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class InventoryOrderList(LibCommonViews.BaseListView):
    model = models.InventoryOrder
    fields = [
        ('id', 'ID'),
        ('customer', 'Customer'),
        ('inventory', 'Inventory'),
        ('comments', 'Comments'),
    ]

    def get_queryset(self):
        # only logged in customer data
        return self.model.objects.filter(customer=self.request.user)


class InventoryOrder(LibCommonViews.BaseDetailView):
    model = models.InventoryOrder
    fields = [
        ('id', 'ID'),
        ('customer', 'Customer'),
        ('inventory', 'Inventory'),
        ('comments', 'Comments'),
    ]

    def get_object(self):
        obj = super(InventoryOrder, self).get_object()
        return obj

    def get_queryset(self):
        # only logged in customer data
        qs = super(InventoryOrder, self).get_queryset().filter(customer=self.request.user)
        return qs


class InventoryOrderCreate(LibCommonViews.BaseCreateView):
    model = models.InventoryOrder
    fields = ['inventory', 'comments']
    success_url = '/orders/'

    def form_valid(self, form):
        user = self.request.user
        form.instance.customer = user
        return super(InventoryOrderCreate, self).form_valid(form)

class InventoryOrderUpdate(LibCommonViews.BaseUpdateView):
    model = models.InventoryOrder
    fields = ['inventory', 'comments']
    success_url = '/orders/'

    def get_queryset(self):
        # only logged in customer data
        qs = super(InventoryOrderUpdate, self).get_queryset().filter(customer=self.request.user)
        return qs