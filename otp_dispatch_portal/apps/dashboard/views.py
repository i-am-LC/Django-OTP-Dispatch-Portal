from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import datetime

from otp_dispatch_portal.apps.client.views import Client

# Create your views here.

# Error pages.
def forbidden_view(request, exception):
    return render(request, '403.html', status=403)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def general_500_error_view(request, exception=None):
    return render(request, '500.html', status=500)

# Project dashboard / landing page. Will only allow access to authorised users.
@login_required
def dashboard(request):

    client_records = Client.objects.all()

    return render(request, 'dashboard/dashboard.html', {'client_records': client_records})