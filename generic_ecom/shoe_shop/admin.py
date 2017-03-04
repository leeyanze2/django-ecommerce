from django.contrib import admin

from shoe_shop import models


class InventoryTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 
                    'created', 'created_by', 'modified', 'modified_by']


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'item_type', 'item_size', 'item_color', 
                    'item_price',
                    'created', 'created_by', 'modified', 'modified_by']


class InventoryOrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'inventory', 'comments',
                    'created', 'created_by', 'modified', 'modified_by']


admin.site.register(models.ExtendedUser)
admin.site.register(models.InventoryType, InventoryTypeAdmin)
admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.InventoryOrder, InventoryOrderAdmin)
