from django.conf.urls import include
from django.urls import path

from .views import *

app_name= 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='homeview'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('blog', BlogView.as_view(), name='blogview'),
    path('product', ProductView.as_view(), name='productview'),
    path('cart', CartView.as_view(), name='cartview'),
    path('logout', UserLogout.as_view(), name='logout'),
]