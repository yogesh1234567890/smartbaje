from decimal import Context
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from orders.models import OrderProduct
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from cart.views import _cart_id
from cart.models import Cart, CartItem
import requests
from django import template

def register(request):
    if request.method == 'POST' and request.is_ajax:
        context = {}
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            context['message'] = 'Password and Confirm Password Do Not Match'
            context['code'] = status.HTTP_400_BAD_REQUEST
            return JsonResponse(context, status=200)
        if Account.objects.filter(email=email).exists():
            context['message'] = 'Email Already Exists'
            context['code'] = status.HTTP_400_BAD_REQUEST
            return JsonResponse(context, status=200)
        else:
            user = Account.objects.create_user(
                full_name=full_name, email=email, password=password)
        
            # USER ACTIVATION
            current_site = get_current_site(request)
            subject = 'Activation Link'
            message = "Attention Please"   
            htmltemp = template.loader.get_template(
                "account_verification_email.html"
            ) 
            c = {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
            html_content = htmltemp.render(c)
            from_email = 'no_reply@smartdeals.com'
            recipient_list=[user.email]
            send_mail(subject, from_email=from_email,recipient_list=recipient_list,message=message, html_message=html_content)
            messages.success(
                request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.')
            context={'message':'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.'}
            return JsonResponse(context, status=200)
            # return redirect('/accounts/login/?command=verification&email='+email)
    else:
        return JsonResponse({'message': 'Invalid Request'}, status=400)

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
            contexts = {'message': 'Invalid Login Details! Please Try Again With A Valid Email And Password'}
            return JsonResponse(contexts, status=400)

        # elif user is not None and not user.is_active:
        #     context['message1'] = 'Sorry, your account is in-Active'
        #     context['message2'] = 'Kindly Check Your Email For Activation Link Or Contact Support'
        #     context['status'] = 'Error!'
        #     context['code']=status.HTTP_401_UNAUTHORIZED
        #     return JsonResponse(context, status = 200)


        elif user is not None:
            try:
                cart = Cart.objects.get(cart = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []

                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    cart_item = CartItem.objects.filter(user=user)
                ex_var_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
                
                for pr in product_variation:
                    if pr in ex_var_list:
                        index = ex_var_list.index(pr)
                        item_id = id[index]
                        item = CartItem.objects.get(id=item_id)
                        item.quantity += 1
                        item.user = user
                        item.save()
                    else:
                        cart_item = CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user = user
                            item.save()

            except:
                pass
            auth.login(request, user)
            context['message'] = 'Successfully authenticated.'
            context['is_superadmin'] = user.is_superadmin
            context['status'] = 'Success!'
            context['code'] = status.HTTP_200_OK
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split('&'))
                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)     

            except:
                if user.is_superadmin:
                    return JsonResponse(context, status=200) 
                else:
                    return JsonResponse(context, status=200)        
        else:
            context['message'] = 'Invalid credentials'
            context['message2'] = 'Kindly Try Again With A Valid Email And Password'
            context['code'] = status.HTTP_401_UNAUTHORIZED
            return JsonResponse(context, status=400)
    return JsonResponse({}, status=200)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('store:store')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        UserProfile.objects.create(user=user)
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('store:store')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('auth:register')



@login_required(login_url = 'login')
def dashboard(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    order_count = OrderProduct.objects.filter(user=request.user).count()
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
        'order_count' : order_count,
    }
    return render(request, 'dashboard.html',context=context)

@login_required(login_url = 'login')
def Profile(request):
    if request.is_ajax():
#         id=request.GET.get('id').title()
        print(request)
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated successfully!')
            return redirect('auth:dashboard')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
        
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
    }
    return render(request, 'profile.html', context=context)

def orders(request):
    if request.is_ajax():
        order_count = OrderProduct.objects.filter(user=request.user).count()
        return render(request, 'orders.html', context={'order_count':order_count})

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            subject = 'Reset Your Password'
            message = "Attention Please" 
            htmltemp = template.loader.get_template(
                "reset_password_email.html"
            ) 
            c = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            html_content = htmltemp.render(c)          
            from_email = 'no_reply@smartdeals.com'
            recipient_list=[user.email]
            send_mail(subject, from_email=from_email,recipient_list=recipient_list,message=message, html_message=html_content)
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('store:store')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('auth:forgotPassword')
    return render(request, 'forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('auth:resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('store:store')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('store:store')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('auth:resetPassword')
    else:
        return render(request, 'resetPassword.html')
