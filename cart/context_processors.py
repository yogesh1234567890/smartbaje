from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user = request.user)
            else:  
                cart_items = CartItem.objects.all().filter(cart = cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count = cart_count)

def cart(request, total=0, quantity=0, cart_items=None,grand_total=0, tax=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
            l=[]
            for i in cart_items:
                if i.product.name not in l:
                    l.append(i.product.name)
            for c in l:
                prod = Product.objects.get(name=c)
                cart_items = CartItem.objects.filter(product = prod)
                if cart_items.count()>1:
                    num=0
                    for i in cart_items:
                        num += i.quantity
                    cart_items.delete()
                    CartItem.objects.create(product=prod, quantity=num, user=request.user)
            cart_items1 = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items1:
            total +=cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax=(2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
        'quantity':quantity,
        'cart_items':cart_items1
    }

    return dict(context)

