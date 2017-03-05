from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import models
from serializers import InventorySerializer, InventoryOrderSerializer


class RestInventoryList(APIView):

    def get(self, request, format=None):
        inventory = models.Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)


class RestInventoryOrder(APIView):

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


class BaseListView(ListView):
    template_name = 'merchants/list.html'

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)

        # self.title handling
        if getattr(self, 'title', None) is None:
            context['title'] = self.model.__name__
        else:
            context['title'] = self.title

        context['fields'] = []
        context['row_data'] = []

        if self.fields is not None:
            for field in self.fields:
                context['fields'].append(field[1])

            for value in context['object_list']:
                current_row = []
                for field in self.fields:
                    if field[0] in value:
                        current_row.append(value[field[0]])
                    else:
                        current_row.append('<data does not exist>')

                context['row_data'].append(current_row)
        else:
            # the below case should only be used for debugging as it just dumps
            # all the data in the object
            if context['object_list'].count() > 0:
                for key, value in context['object_list'][0].__dict__.iteritems():
                    if not(str(key).startswith("_") or str(key).startswith("id")):
                        context['fields'].append(key)
            for value in context['object_list']:
                current_row = []
                for field_name in context['fields']:
                    current_row.append(getattr(value, field_name))
                context['row_data'].append(current_row)

        return context


class InventoryOrderList(BaseListView):
    model = models.InventoryOrder
