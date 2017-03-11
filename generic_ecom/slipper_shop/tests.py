from django.utils import timezone

from django.test import TestCase, Client
from django.forms.models import model_to_dict

from .model_user import ExtendedUser
from . import models


class SlippersShopTest(TestCase):

    def setUp(self):
        # creating logged in user
        self.loggedin_user = ExtendedUser.objects.create_user(
            username='fred',
            password='secret',
            email='fred@fred.com'
        )

        self.user_count = ExtendedUser.objects.count()

        self.c = Client()
        self.c.login(username='fred', password='secret')

        # todo:mal: really ought to use Fixtures but just setting it up manually due to lack of time
        # self.audit_log_vars = {}
        # self.audit_log_vars['created'] = timezone.now()
        # self.audit_log_vars['modified'] = timezone.now()
        # self.audit_log_vars['created_by'] = self.loggedin_user
        # self.audit_log_vars['modified_by'] = self.loggedin_user

        inventory_type_vars = {}
        inventory_type_vars['name'] = "Running"
        # inventory_type_vars.update(self.audit_log_vars)
        self.inventory_type = models.InventoryType(**inventory_type_vars)
        self.inventory_type.save()

        inventory_vars = {}
        inventory_vars['sku'] = "item-1"
        inventory_vars['name'] = "Nike Slippers"
        inventory_vars['item_type'] = self.inventory_type
        inventory_vars['item_size'] = 2
        # inventory_vars['item_color'] = 'B1' # because this is not shoe
        inventory_vars['item_price'] = 64.00
        # inventory_vars.update(self.audit_log_vars)
        self.inventory = models.Inventory(**inventory_vars)
        self.inventory.save()

        inventory_order_vars = {}
        inventory_order_vars['customer'] = self.loggedin_user
        inventory_order_vars['inventory'] = self.inventory
        inventory_order_vars['comments'] = "goood"
        # inventory_order_vars.update(self.audit_log_vars)
        self.inventory_order = models.InventoryOrder(**inventory_order_vars)
        self.inventory_order.save()

    def test_list(self):
        response = self.c.get('/orders/')

        # testing page integrity
        self.assertEqual(response.status_code, 200)

        # testing data integrity
        rows_of_data = len(response.context['row_data'])
        self.assertEqual(rows_of_data, 1)

    def test_view(self):
        response = self.c.get('/order/' + str(self.inventory_order.id) + '/')

        # testing page integrity
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        new_data = {}
        new_data['customer'] = self.loggedin_user
        new_data['inventory'] = self.inventory.id
        new_data['comments'] = "baad"

        response = self.c.get('/orders/add/')

        # testing page integrity
        self.assertEqual(response.status_code, 200)

        # testing data integrity
        original_count = models.InventoryOrder.objects.count()
        response = self.c.post('/orders/add/', new_data)
        self.assertEqual(models.InventoryOrder.objects.count(),
                         original_count + 1)

    def test_update(self):
        obj = models.InventoryOrder.objects.get(pk=self.inventory_order.id)
        obj_dict = model_to_dict(obj)

        response = self.c.get(
            '/order/edit/' + str(self.inventory_order.id) + '/')

        # testing page integrity
        self.assertEqual(response.status_code, 200)

        # testing data integrity
        original_comments = obj_dict["comments"]
        obj_dict["comments"] = original_comments + "_changed"
        response = self.c.post(
            '/order/edit/' + str(self.inventory_order.id) + '/', obj_dict)

        new_obj = models.InventoryOrder.objects.get(pk=obj.id)
        self.assertEqual(new_obj.comments, original_comments + "_changed")

    def test_delete(self):
        obj = models.InventoryOrder.objects.get(pk=self.inventory_order.id)
        obj_dict = model_to_dict(obj)

        response = self.c.get(
            '/order/delete/' + str(self.inventory_order.id) + '/')

        # testing page integrity
        self.assertEqual(response.status_code, 200)

        # testing data integrity
        original_count = models.InventoryOrder.objects.count()
        response = self.c.post(
            '/order/delete/' + str(self.inventory_order.id) + '/')

        self.assertEqual(models.InventoryOrder.objects.count(),
                         original_count - 1)
