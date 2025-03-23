from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('electronics/', views.electronics, name='electronics'),
    path('fashion/', views.fashion, name='fashion'),
    path('furniture/', views.furniture, name='furniture'),
    path('mobile/', views.mobile, name='mobile'),
    path('laptop/', views.laptop, name='laptop'),
    path('men/', views.men, name='men'),
    path('women/', views.women, name='women'),
    path('bed/', views.bed, name='bed'),
    path('cupboard/', views.cupboard, name='cupboard'),
    path('shirt/', views.shirt, name='shirt'),
    path('men_shoes/', views.men_shoes, name='men_shoes'), 
    path('women_shoes/', views.women_shoes, name='women_shoes'), 
    path('sarees/', views.sarees, name='sarees'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-placed/', views.order_placed, name='order_placed'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
     path('accounts/login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name='login'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
