from basketapp.models import Basket


def basket(request):
    basket_items = []
    if request.user.is_authenticated:
        basket_items = Basket.objects.filter(user=request.user).select_related()
    return {
        'basket_list': basket_items,
        'basket_total_quantity': sum(list(map(lambda x: x.quantity, basket_items))),
        'basket_total_cost': sum(list(map(lambda x: x.product.price * x.quantity, basket_items))),
    }








