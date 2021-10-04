from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from cart.views import _cart_id
from cart.models import Cart, CartItem
import requests


def register(request):
    if request.method == 'POST' and request.is_ajax:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = first_name+" "+last_name
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            # current_site = get_current_site(request)
            # mail_subject = 'Please activate your account'
            # message = render_to_string('accounts/account_verification_email.html', {
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()
            messages.success(
                request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('auth:register')
            # return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return context


def login(request):
    if request.method == 'POST' and request.is_ajax:
        context = {}
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is None:
            context['message1'] = 'Invalid Login Details!'
            context['message2'] = 'Please Try Again With A Valid Email And Password'
            context['code'] = status.HTTP_401_UNAUTHORIZED
            return JsonResponse(context, status=200)

        # elif user is not None and not user.is_active:
        #     context['message1'] = 'Sorry, your account is in-Active'
        #     context['message2'] = 'Kindly Check Your Email For Activation Link Or Contact Support'
        #     context['status'] = 'Error!'
        #     context['code']=status.HTTP_401_UNAUTHORIZED
        #     return JsonResponse(context, status = 200)


        elif user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(
                    cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    # product_variation = []
                    for item in cart_item:
                        item.user = user
                        item.save()
                    #     variation = item.variations.all()
                    #     product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    # cart_item = CartItem.objects.filter(user=user)
                    # ex_var_list = []
                    # id = []
                    # for item in cart_item:
                    #     existing_variation = item.variations.all()
                    #     ex_var_list.append(list(existing_variation))
                    #     id.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]

            #         for pr in product_variation:
            #             if pr in ex_var_list:
            #                 index = ex_var_list.index(pr)
            #                 item_id = id[index]
            #                 item = CartItem.objects.get(id=item_id)
            #                 item.quantity += 1
            #                 item.user = user
            #                 item.save()
            #             else:
            #                 cart_item = CartItem.objects.filter(cart=cart)
            #                 for item in cart_item:
            #                     item.user = user
            #                     item.save()
            except:
                pass
            auth.login(request, user)
            context['message'] = 'Successfully authenticated.'
            context['status'] = 'Success!'
            context['code'] = status.HTTP_200_OK
            messages.success(request, 'You are now logged in.')
            return JsonResponse(context, status=200)        
        else:
            context['message'] = 'Invalid credentials'
            context['message2'] = 'Kindly Try Again With A Valid Email And Password'
            context['code'] = status.HTTP_401_UNAUTHORIZED
            return JsonResponse(context, status=200)
    return JsonResponse({}, status=200)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('store:store')
