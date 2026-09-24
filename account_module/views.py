from django.shortcuts import render
from django.contrib.auth import get_user_model

user = get_user_model()

def user_view(request):
    first_name = user.first_name

