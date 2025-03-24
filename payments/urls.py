from django.urls import path
from .views import home, user_details, payment_purpose, payment_page, process_payment, payment_success

urlpatterns = [
    path('', home, name='home'),
    path('user-details/', user_details, name='user_details'),
    path('payment-purpose/', payment_purpose, name='payment_purpose'),
    path('payment/', payment_page, name='payment_page'),
    path('process-payment/', process_payment, name='process_payment'),
    path('payment-success/', payment_success, name='payment_success'),
]
