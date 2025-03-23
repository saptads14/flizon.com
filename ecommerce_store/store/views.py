from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.conf import settings
from .forms import CustomerRegisterForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product
from store.models import Product 
from decimal import Decimal

@login_required
def order_placed(request):
    return render(request, 'store/order_placed.html')


@login_required
def cart(request):
    cart = request.session.get('cart', [])
    cart_items = []
    total = 0

    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        total_price = product.price * item['quantity']
        total += total_price
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'total_price': total_price
        })

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'store/cart.html', context)



@login_required
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect('home')

    cart = request.session.get('cart', [])
    
    # Debugging: Print current cart items
    print("Current cart items:", cart)

    # Flag to track if the product is already in the cart
    product_in_cart = False

    # Update cart with new quantity if product exists
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            product_in_cart = True
            break

    # Add new product to the cart
    if not product_in_cart:
        cart.append({'product_id': product_id, 'quantity': 1})

    # Save cart to session
    request.session['cart'] = cart
    request.session.modified = True  # Ensure session is saved

    # Debugging: Print updated cart items
    print("Updated cart items:", request.session.get('cart', []))

    return redirect('cart')





@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    # Remove the product from the cart if found
    cart = [item for item in cart if item['product_id'] != product_id]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')





def home(request):
    return render(request, 'store/home.html')

def electronics(request):
    return render(request, 'store/electronics.html')

def fashion(request):
    return render(request, 'store/fashion.html')

def furniture(request):
    return render(request, 'store/furniture.html')

def mobile(request):
    return render(request, 'store/mobile.html')

def laptop(request):
    return render(request, 'store/laptop.html')

def men(request):
    return render(request, 'store/men.html')

def women(request):
    return render(request, 'store/women.html')

def bed(request):
    return render(request, 'store/bed.html')

def cupboard(request):
    return render(request, 'store/cupboard.html')

def shirt(request):
    return render(request, 'store/shirt.html')

def men_shoes(request):
    return render(request, 'store/men_shoes.html') 

def women_shoes(request):
    return render(request, 'store/women_shoes.html')

def sarees(request):
    return render(request, 'store/sarees.html')

@login_required
def checkout(request):
    cart = request.session.get('cart', [])
    total = Decimal('0.00')

    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        total_price = product.price * item['quantity']
        total += total_price

    cgst = total * Decimal('0.05')
    sgst = total * Decimal('0.05')
    grand_total = total + cgst + sgst

    context = {
        'total': total,
        'cgst': cgst,
        'sgst': sgst,
        'grand_total': grand_total
    }

    return render(request, 'store/checkout.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to the login page or any other page
    else:
        return redirect('home') 
    
    # Base view
def base_view(request):
    return render(request, 'store/base.html')

# Customer Registration View
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegisterForm()
        return render(request, 'store/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! User registration successful.')
            return redirect('home')  # Redirect to home or another appropriate page
        else:
            messages.warning(request, 'Unsuccessful registration. Invalid information.')
        return render(request, 'store/customerregistration.html', {'form': form})

################ password reset ################################################ 
def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "store/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': 'yourdomain.com',
                        'site_name': 'Your Site',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@yourdomain.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect('login')
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request, 'store/password_reset_form.html', {'form': password_reset_form, 'title': 'Password Reset'})

def password_reset_confirm(request, uidb64=None, token=None):
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been set. You may go ahead and log in now.')
            return redirect('login')
    else:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user)
        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return redirect('password_reset')
    return render(request, 'store/password_reset_confirm.html', {'form': form, 'title': 'Set New Password'})

def password_reset_done(request):
    return render(request, 'store/password_reset_done.html', {'title': 'Password Reset Done'})

def password_reset_complete(request):
    return render(request, 'store/password_reset_complete.html', {'title': 'Password Reset Complete'})


def custom_logout_view(request):
    logout(request)
    return redirect(request, 'user/logout.html')

def send_email_view(request):
    subject = "Subject"
    message = "Message"
    from_email = "from@example.com"
    recipient_list = ["to@example.com"]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return HttpResponse('Email sent successfully.')


