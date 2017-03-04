from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractUser

from enumfields import EnumField
from enumfields import Enum

from djmoney.models.fields import MoneyField


# @python_2_unicode_compatible
class ExtendedUser(AbstractUser):
    mailing_address = models.TextField()
    billing_address = models.TextField()


class BaseModel(models.Model):
    """BaseModel has audit log handling"""
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
    created_by = models.ForeignKey(
        ExtendedUser, related_name="%(app_label)s_%(class)s_created_by_user", editable=False)
    modified_by = models.ForeignKey(
        ExtendedUser, related_name="%(app_label)s_%(class)s_modified_by_user", editable=False)

    class Meta:
        abstract = True


class Color(Enum):
    DARK_BLUE = 'B1'
    LIGHT_BLUE = 'B2'
    YELLOW = 'Y1'

    class Labels:
        DARK_BLUE = _('Dark Blue')
        LIGHT_BLUE = _('Light Blue')
        YELLOW = _('Yellow')


@python_2_unicode_compatible
class InventoryType(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# @python_2_unicode_compatible
class Inventory(BaseModel):
    sku = models.CharField(max_length=30, unique=True, db_index=True)
    # indexing for inevitable search requirement
    name = models.CharField(max_length=100, db_index=True)
    item_type = models.ForeignKey(InventoryType)
    item_size = models.PositiveSmallIntegerField()
    item_color = EnumField(Color, max_length=2)
    # if we are strictly storing only USD, probably this config for max digits
    # and decimals will be sufficient
    item_price = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD')

    def __str__(self):
        return "(" + self.sku + ") "+ self.name


# @python_2_unicode_compatible
class InventoryOrder(BaseModel):
    customer = models.ForeignKey(ExtendedUser)
    inventory = models.ForeignKey(Inventory)
    comments = models.TextField(blank=True, default="")
