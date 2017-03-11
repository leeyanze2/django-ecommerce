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


class RestInventoryOrder(LibCommonViews.BaseRestInventoryOrder):
    def initial(self, request, *args, **kwargs):
        # setting the params so can refactor into a common parent
        kwargs['nv_params'] = {}
        kwargs['nv_params']['models'] = models
        kwargs['nv_params'][
            'InventoryOrderSerializer'] = InventoryOrderSerializer
        super(RestInventoryOrder, self).initial(request, *args, **kwargs)


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
        qs = super(InventoryOrder, self).get_queryset().filter(
            customer=self.request.user)
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
        qs = super(InventoryOrderUpdate, self).get_queryset().filter(
            customer=self.request.user)
        return qs


class InventoryOrderDelete(LibCommonViews.BaseDeleteView):
    model = models.InventoryOrder
    success_url = '/orders/'

    def get_queryset(self):
        # only logged in customer data
        qs = super(InventoryOrderDelete, self).get_queryset().filter(
            customer=self.request.user)
        return qs
