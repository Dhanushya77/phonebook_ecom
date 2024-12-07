from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_login),
    path('user_logout',views.user_logout),
    path('register/',views.register),
    path('otp',views.otp_confirmation),
    path('phonebook',views.phonebook),
    path('add_contact/<id>',views.add_contact),
    path('delete_contact/<id>',views.delete_contact),
    path('edit_contact/<id>',views.edit_contact),
]