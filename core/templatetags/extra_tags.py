from django import template
register = template.Library()  
from ..models import AddtoCard, OrderItem, User, Product, Category

@register.filter
def addto_card_items(user_id):
    order_items = OrderItem.objects.filter(user_id=user_id).count()
    return order_items


@register.filter
def category(self):
    product = Category.objects.all()
    return product


@register.filter
def check_card(product_id,user_id):
    ob = OrderItem.objects.filter(product_id=product_id, user_id=user_id)
    if ob.exists():
        return 1
    else:
        return 2

# @@register.filter
# def login(value):
#     return value
