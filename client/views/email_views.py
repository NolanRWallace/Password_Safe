from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..models import User, Combo, Emails, Passwords
import bcrypt