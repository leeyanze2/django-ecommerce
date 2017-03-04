from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from models import Inventory, ExtendedUser, InventoryOrder
from serializers import InventorySerializer, InventoryOrderSerializer


@api_view(['GET'])
def inventory_list(request):
    """List all Inventory items"""
    if request.method == 'GET':
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def order(request):
    """ Current user will place order"""
    inventory_id = request.data.get('inventory_id', None)

    user_id = None
    if hasattr(request, 'user'):
        user_id = request.user.id

    if inventory_id is not None and user_id is not None:
        try:
            inventory_item = Inventory.objects.get(pk=inventory_id)
        except Inventory.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user = ExtendedUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            new_data = {}
            new_data['inventory'] = inventory_item
            new_data['customer'] = user
            new_order = InventoryOrder(**new_data)
            new_order.save()

            return Response(InventoryOrderSerializer(new_order).data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)
