
# Create your views here.
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone


def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def landing(request):
    return render(request, 'home/landing.html')

# def about_para(request):
#     return render(request, 'home/about_para.html')
