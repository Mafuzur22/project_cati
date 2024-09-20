from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('donate/', views.donate, name="DonationPage"),
    path('donate/payment/', views.payment, name="PaymentProced"),
    path('donationok', views.donation_done, name="DonationSent")
]