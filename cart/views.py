from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from accounts.models import UserProfile
from store.models import Product, Variation
from cart.models import Cart, CartItem
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def _cart_id(request):  # private function with _
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
    
def add_cart(request, product_id):
    value = request.POST.dict()
    print(value)
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                print('key::: ',key, 'value::: ',value)

                # try:
                #     variation_all = Variation.objects.all()
                #     # print("get all variation::: ", variation_all)
                #     variation = get_object_or_404(Variation, variation_category__iexact = key, variation_value__iexact = value)
                #     print("variations::: ", variation)
                #     print("variations::: ", type(variation))
                #     product_variation.append(variation)
                #     print("getting variation list::: ", product_variation)

                # except Exception as e:
                #     # print("error occured::: ", e)
                #     pass
            # return HttpResponse(color + ' ' + size)
        # product = Product.objects.get(id=product_id)

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        print("is cart item exists::: ", is_cart_item_exists)
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            print("is cart item::: ", cart_item)
            
            '''
            existing variations => getting from database
            current variation => getting from product variation list
            item_id => getting from database
            '''
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print("printing exisiting var list::: ",ex_var_list)

            print("product variation list in ex_var_list::: ", product_variation in ex_var_list)
            # try:
            if product_variation in ex_var_list:
                '''increase the cart item quantity'''
                index = ex_var_list.index(product_variation)
                print("index no getting::: ", index)
                item_id = id[index]
                print("item_id::: ", item_id)
                item = get_object_or_404(CartItem, product=product, id = item_id)
                print("getting item from cart item::: ", item)
                item.quantity += 1
                print("if of saving item/final item data::: ",item.save())

            
            else:
            # except:
                print("user::: ", request.user)
                item = CartItem.objects.create(product = product, quantity = 1, user=current_user)
                print("Getting Item::: ", item)
                print(product_variation)
                if len(product_variation) > 0:
                    # item.variations.clear()
                    print("product variation:: ", item.variations)
                    for i in product_variation:
                        print(type(product_variation), i)
                    item.variations.add(*product_variation)
                    item.save()
                # cart_item.quantity += 1
                print(item)
                print(item.variations)
                # print("else of saving item/final item data::: ",)

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=current_user,
            )
            if len(product_variation) > 0:
                # cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        # return HttpResponse("Product Name::: "+ str(cart_item.product) +"===>"+  "Product Quantity::: " + str(cart_item.quantity))
        return redirect('cart:cart')
    #for anonymomus user    
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                print('key::: ',key, 'value::: ',value)

                try:
                    variation = get_object_or_404(Variation, variation_category__iexact = key, variation_value__iexact = value)
                    print("variations::: ", variation)
                    product_variation.append(variation)

                except:
                    pass
            # return HttpResponse(color + ' ' + size)
        product = Product.objects.get(id=product_id)
        print("Get product id::: ", product)
        try:
            print("try block part working")
            cart = Cart.objects.get(cart = _cart_id(request)) #get the cart using  cart field present in the session
            print("Cart:::", cart)
        except Cart.DoesNotExist:
            print("Exception part working")
            cart = Cart.objects.create(
                cart = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            '''
            existing variations => getting from database
            current variation => getting from product variation list
            item_id => getting from database
            '''
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)

            if product_variation in ex_var_list:
                '''increase the cart item quantity'''
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id = item_id)
                item.quantity += 1
                item.save()
            
            else:
                item = CartItem.objects.create(product = product, quantity = 1, cart = cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                # cart_item.quantity += 1
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        # return HttpResponse("Product Name::: "+ str(cart_item.product) +"===>"+  "Product Quantity::: " + str(cart_item.quantity))
        return redirect('cart:cart')

def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart:cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart:cart')


def cart(request, total=0, quantity=0, cart_items=None, grand_total=0, tax=0):
    try:
        if request.user.is_authenticated:
            # print("user::: ", request.user)
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'quantity': quantity,
        'cart_items': cart_items
    }

    return render(request, 'cart/cart.html', context)


@login_required(login_url='auth:login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        userprofile = get_object_or_404(UserProfile, user=request.user)
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        'user_data': userprofile
    }
    return render(request, 'cart/checkout.html', context)
