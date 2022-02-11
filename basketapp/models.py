from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    @cached_property
    def get_item(self):
        return self.user.basket.select_related()

    @property
    def cost_product(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        items = self.get_item
        _total_quantity = sum(list(map(lambda x: x.quantity, items)))
        return _total_quantity

    @property
    def total_cost(self):
        items = self.get_item
        _total_cost = sum(list(map(lambda x: x.cost_product, items)))
        return _total_cost

