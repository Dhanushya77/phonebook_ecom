from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from.models import *
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
# ------------------user login-------------------------


def user_login(req):
    if req.method == 'POST':
        uname = req.POST['uname']
        password = req.POST['password']
        user = authenticate(username=uname,password=password)
        if user:
            login(req,user)
            return redirect(phonebook)
        else:
            messages.warning(req,'Invalid username or password')
            return redirect(user_login)
    return render(req,'login.html')


# --------------------user logout---------------------------


def user_logout(req):
    logout(req)
    return redirect(user_login)


# -------------------user registration------------------------


def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswrd=req.POST['pswrd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswrd)
            data.save()
            send_mail('Registration','Registration successful', settings.EMAIL_HOST_USER, [email])
            return redirect(user_login)
        except:
            messages.warning(req,'Email already exist')
            return redirect(register)
    else:
        return render(req,'register.html')


def phonebook(req):
    data=Phonebook.objects.filter(user=req.user)
    return render(req,'phonebook.html',{'data':data})

def add_contact(req,id):
    if req.method=='POST':
        user = User.objects.get(pk=id)
        name = req.POST['name']
        phn_num = req.POST['phn_num']
        data = Phonebook.objects.create(user=user,name=name,phn_num=phn_num)
        data.save()
        return redirect(phonebook)
    return render(req,'add_contact.html')

def edit_contact(req,id):
    data = Phonebook.objects.get(pk=id)   
    if req.method == 'POST':
        name = req.POST['name']
        phn_num = req.POST['phn_num']
        Phonebook.objects.filter(pk=id).update(name=name,phn_num=phn_num)
        return redirect(phonebook)
    else:
        return render(req,'edit_contact.html',{'data':data})

def delete_contact(req,id):
    data = Phonebook.objects.get(pk=id)
    data.delete()
    return redirect(phonebook)