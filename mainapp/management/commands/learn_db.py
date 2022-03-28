from django.db.models import F, Q, When, Case, DecimalField, IntegerField
from datetime import timedelta
from django.core.management import BaseCommand
from ordersapp.models import OrderItem


class Command(BaseCommand):

    def handle(self, *args, **options):
        action_1 = 1
        action_2 = 2
        action_3 = 3

        action_1_timedelta = timedelta(hours=12)
        action_2_timedelta = timedelta(days=1)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.1

        action_1_condition = Q(order__updated_at__lte=F('order__created_at') + action_1_timedelta)
        action_2_condition = Q(order__updated_at__gt=F('order__created_at') + action_1_timedelta) & \
                             Q(order__updated_at__lte=F('order__created_at') + action_2_timedelta)
        action_3_condition = Q(order__updated_at__gt=F('order__created_at') + action_2_timedelta)

        action_1_order = When(action_1_condition, then=action_1)
        action_2_order = When(action_2_condition, then=action_2)
        action_3_order = When(action_3_condition, then=action_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        test_order = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField(),
            )
        ).annotate(
            action_price=Case(
                action_1_price,
                action_2_price,
                action_3_price,
                output_field=DecimalField(),
            )
        )
        for orderitem in test_order:
            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}:\
                   {orderitem.product.name:15}: скидка\
                   {abs(orderitem.action_price):6.2f} руб. | \
                   {orderitem.order.updated_at - orderitem.order.created_at}')
