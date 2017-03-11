from rest_framework import serializers
from drf_enum_field.serializers import EnumFieldSerializerMixin

from models import Inventory, InventoryOrder


class InventorySerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('__all__')


class InventoryOrderSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = InventoryOrder
        fields = ('__all__')
