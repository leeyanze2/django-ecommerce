from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractUser

from enumfields import EnumField
from enumfields import Enum

from djmoney.models.fields import MoneyField

from lib_common.models import BaseModel, BaseInventoryType
from model_user import ExtendedUser


# class Color(Enum):
#     DARK_BLUE = 'B1'
#     LIGHT_BLUE = 'B2'
#     YELLOW = 'Y1'

#     class Labels:
#         DARK_BLUE = _('Dark Blue')
#         LIGHT_BLUE = _('Light Blue')
#         YELLOW = _('Yellow')


class InventoryType(BaseInventoryType):
    """ Probably a  pointless refactor to use a parent class, just performing it to demonstrate"""
    pass


# @python_2_unicode_compatible
class Inventory(BaseModel):
    sku = models.CharField(max_length=30, unique=True, db_index=True)
    # indexing for inevitable search requirement
    name = models.CharField(max_length=100, db_index=True)
    item_type = models.ForeignKey(InventoryType)
    item_size = models.PositiveSmallIntegerField()
    # item_color = EnumField(Color, max_length=2) # because this is not shoe
    # if we are strictly storing only USD, probably this config for max digits
    # and decimals will be sufficient
    item_price = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD')

    def __str__(self):
        return "(" + self.sku + ") " + self.name


# @python_2_unicode_compatible
class InventoryOrder(BaseModel):
    customer = models.ForeignKey(ExtendedUser)
    inventory = models.ForeignKey(Inventory)
    comments = models.TextField(blank=True, default="")
