from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from.models import *
from django.conf import settings
from django.core.mail import send_mail
import random

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
            otp=""
            for i in range(6):
                otp+=str(random.randint(0,9))
            msg=f'Your registration is completed otp: {otp}'
            send_mail('Registration',otp, settings.EMAIL_HOST_USER, [email])
            Otp.objects.create(user=data,otp=otp)
            return redirect(otp_confirmation)
        except:
            messages.warning(req,'Email already exist')
            return redirect(register)
    else:
        return render(req,'register.html')


def otp_confirmation(req):
    if req.method == 'POST':
        uname = req.POST.get('uname')
        user_otp = req.POST.get('otp')
        try:
            user = User.objects.get(username=uname)
            generated_otp = Otp.objects.get(user=user)
    
            if generated_otp.otp == user_otp:
                generated_otp.delete()
                return redirect(user_login)
            else:
                messages.warning(req, 'Invalid OTP')
                return redirect(otp_confirmation)
        except User.DoesNotExist:
            messages.warning(req, 'User does not exist')
            return redirect(otp_confirmation)
        except Otp.DoesNotExist:
            messages.warning(req, 'OTP not found or expired')
            return redirect(otp_confirmation)
    return render(req, 'otp.html')


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