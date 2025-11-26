from django.shortcuts import render, redirect, get_object_or_404
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
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product, Order, OrderItem, Address
from decimal import Decimal
from django.views.decorators.http import require_POST
from .models import Address
from django.db import transaction
from django.utils import timezone
import uuid
from decimal import Decimal


def language(request):
    languages = [
        {'name': 'English', 'flag': 'images/flags/english.png'},
        {'name': 'Hindi', 'flag': 'images/flags/hindi.png'},
        {'name': 'Spanish', 'flag': 'images/flags/spanish.png'},
        {'name': 'French', 'flag': 'images/flags/french.png'},
        {'name': 'German', 'flag': 'images/flags/german.png'},
        {'name': 'Chinese', 'flag': 'images/flags/chinese.png'},
        {'name': 'Japanese', 'flag': 'images/flags/japanese.png'},
    ]
    context = {
        'languages': languages
    }
    
    return render(request, 'store/language.html', context)


@login_required
def order_placed(request):
    return render(request, 'store/order_placed.html')


########################-- Wishlist Page --#########################
# wishlist page
@login_required
def wishlist(request):
    # Retrieve wishlist data from session
    wishlist = request.session.get('wishlist', [])
    wishlist_items = []

    for item in wishlist:
        product = get_object_or_404(Product, id=item['product_id'])
        wishlist_items.append({
            'product': product,
        })

    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': len(wishlist),  # ✅ number of items in wishlist
    }

    return render(request, 'store/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect('index')

    wishlist = request.session.get('wishlist', [])

    # Debugging: Print current wishlist items
    print("Current wishlist items:", wishlist)

    # Check if product already exists in wishlist
    product_in_wishlist = any(item['product_id'] == product_id for item in wishlist)

    if not product_in_wishlist:
        wishlist.append({'product_id': product_id})
        messages.success(request, f'{product.name} added to your wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')

    # Save wishlist to session
    request.session['wishlist'] = wishlist
    request.session.modified = True  # Ensure session is saved

    # Debugging: Print updated wishlist items
    print("Updated wishlist items:", request.session.get('wishlist', []))

    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])

    # Remove the product from the wishlist if found
    wishlist = [item for item in wishlist if item['product_id'] != product_id]

    request.session['wishlist'] = wishlist
    request.session.modified = True
    messages.success(request, 'Item removed from wishlist.')

    return redirect('wishlist')


########################-- Cart Page --#########################
# cart page
@login_required
def cart(request):
    # Retrieve cart data from session
    cart = request.session.get('cart', [])
    cart_items = []
    total = 0
    total_quantity = 0

    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        quantity = item.get('quantity', 1)
        total_price = product.price * quantity
        total += total_price
        total_quantity += quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': total_quantity,  # ✅ number of items in cart
    }

    return render(request, 'store/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """
    Adds a product to the cart.

    Args:
        request: The current request object.
        product_id: The ID of the product to add to the cart.

    Returns:
        A redirect to the cart page.
    """
    try:
        product = get_object_or_404(Product, id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect('index')

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


# home page or index page
def home(request):
    return render(request, 'store/index.html')

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
    addresses = Address.objects.filter(user=request.user)

    # You might already calculate totals
    total = 1000
    cgst = total * 0.05
    sgst = total * 0.05
    grand_total = total + cgst + sgst

    context = {
        'addresses': addresses,
        'total': total,
        'cgst': cgst,
        'sgst': sgst,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  
    else:
        return redirect('home') 
    

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



@login_required
@transaction.atomic
def order_placed(request):
    """
    Handles POST from checkout page, creates Order + OrderItem(s).
    Robust to different session-cart shapes:
      - dict keyed by product_id: { '1': {'qty':2,'price':100}, ... }
      - list of items: [ {'product_id':1,'qty':2,'price':100}, ... ]
      - (optional) Cart/CartItem models (commented)
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    user = request.user
    addr_id = request.POST.get('selected_address') or request.POST.get('hidden_selected_address')
    payment_method = request.POST.get('payment_method') or request.POST.get('hidden_payment_method')

    # Basic validation
    if not addr_id:
        messages.error(request, "Please select a delivery address.")
        return redirect('checkout')
    if not payment_method:
        messages.error(request, "Please select a payment method.")
        return redirect('checkout')

    # Fetch and validate address
    try:
        shipping_address = Address.objects.get(id=addr_id, user=user)
    except Address.DoesNotExist:
        messages.error(request, "Selected address not found.")
        return redirect('checkout')

    # Load cart from session (or from DB if you use Cart model)
    session_cart = request.session.get('cart')  # could be dict or list
    cart_items = []  # will hold tuples (product_obj, qty, price)

    if session_cart:
        # If it's a dict-like mapping (common)
        if isinstance(session_cart, dict):
            for pid, pdata in session_cart.items():
                try:
                    prod = Product.objects.select_for_update().get(pk=pid)
                except Product.DoesNotExist:
                    # skip missing products
                    continue
                # pdata might be dict with 'qty' and optionally 'price'
                qty = int(pdata.get('qty', 1)) if isinstance(pdata, dict) else int(pdata)
                price = pdata.get('price') if isinstance(pdata, dict) else prod.price
                cart_items.append((prod, qty, Decimal(str(price))))
        # If it's a list of item dicts (some code stores this shape)
        elif isinstance(session_cart, list):
            for entry in session_cart:
                # support two possible keys: 'product_id' or 'id'
                pid = entry.get('product_id') or entry.get('id') or entry.get('pk')
                if pid is None:
                    # maybe it's a list of product ids: entry == pid
                    if isinstance(entry, (int, str)):
                        pid = entry
                        qty = 1
                        price = None
                    else:
                        continue
                try:
                    prod = Product.objects.select_for_update().get(pk=pid)
                except Product.DoesNotExist:
                    continue
                qty = int(entry.get('qty', 1))
                price = entry.get('price') if entry.get('price') is not None else prod.price
                cart_items.append((prod, qty, Decimal(str(price))))
        else:
            try:
                for pid, pdata in session_cart.items():
                    try:
                        prod = Product.objects.select_for_update().get(pk=pid)
                    except Product.DoesNotExist:
                        continue
                    qty = int(pdata.get('qty', 1))
                    price = pdata.get('price') or prod.price
                    cart_items.append((prod, qty, Decimal(str(price))))
            except Exception:
                # log for debugging
                print("order_placed: unexpected session_cart type:", type(session_cart), session_cart)
                messages.error(request, "Cart format not recognized. Please try again.")
                return redirect('checkout')
    else:
        # Optionally handle Cart model (if you use it) - uncomment and adapt
        """
        try:
            cart = Cart.objects.get(user=user)
            items_qs = CartItem.objects.filter(cart=cart).select_related('product').select_for_update()
            for ci in items_qs:
                cart_items.append((ci.product, ci.quantity, ci.product.price))
        except Cart.DoesNotExist:
            cart_items = []
        """
        messages.error(request, "Your cart is empty.")
        return redirect('home')

    # If cart_items empty after processing
    if not cart_items:
        messages.error(request, "Your cart is empty or items are invalid.")
        return redirect('home')

    # Calculate totals server-side
    subtotal = Decimal('0.00')
    for prod, qty, price in cart_items:
        price = Decimal(price)
        subtotal += price * qty

    cgst = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
    sgst = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
    grand_total = (subtotal + cgst + sgst).quantize(Decimal('0.01'))

    # Create order
    order_number = uuid.uuid4().hex[:12].upper()
    order = Order.objects.create(
        user=user,
        order_number=order_number,
        shipping_address=shipping_address,
        payment_method=payment_method,
        subtotal=subtotal,
        cgst=cgst,
        sgst=sgst,
        total=grand_total,
        status='placed',
        created_at=timezone.now(),
    )

    # Create order items and decrement stock
    for prod, qty, price in cart_items:
        # ensure enough stock
        if hasattr(prod, 'stock') and prod.stock is not None:
            if prod.stock < qty:
                transaction.set_rollback(True)
                messages.error(request, f"Insufficient stock for {prod.name}. Available: {prod.stock}")
                return redirect('checkout')

        OrderItem.objects.create(
            order=order,
            product=prod,
            product_name=prod.name,
            quantity=qty,
            price=price,
            total_price=(price * qty).quantize(Decimal('0.01'))
        )

        if hasattr(prod, 'stock') and prod.stock is not None:
            prod.stock = prod.stock - qty
            if prod.stock < 0:
                prod.stock = 0
            prod.save()

    # Clear session cart (if used)
    if 'cart' in request.session:
        try:
            del request.session['cart']
            request.session.modified = True
        except KeyError:
            pass

    messages.success(request, f"Order placed successfully! Order no: {order_number}")
    return redirect('order_placed')  



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, "Thanks — your message has been received.")
        return redirect('contact')

    return render(request, 'store/contact.html')


@login_required
def add_address(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        line1 = request.POST.get('line1')
        line2 = request.POST.get('line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        is_default = request.POST.get('is_default') == 'on'

        if is_default:
            Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            line1=line1,
            line2=line2,
            city=city,
            state=state,
            pincode=pincode,
            is_default=is_default
        )
    return redirect('checkout')


@login_required
def edit_address(request):
    if request.method == 'POST':
        addr_id = request.POST.get('addr_id')
        address = get_object_or_404(Address, id=addr_id, user=request.user)

        address.full_name = request.POST.get('full_name')
        address.line1 = request.POST.get('line1')
        address.line2 = request.POST.get('line2')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.pincode = request.POST.get('pincode')
        address.phone = request.POST.get('phone')
        is_default = request.POST.get('is_default') == 'on'
        if is_default:
            Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        address.is_default = is_default
        address.save()
        messages.success(request, "Address updated successfully!")
    return redirect('checkout')


@login_required
def delete_address(request):
    if request.method == 'POST':
        addr_id = request.POST.get('addr_id')
        address = get_object_or_404(Address, id=addr_id, user=request.user)
        address.delete()
        messages.success(request, "Address removed successfully!")
    return redirect('checkout')

