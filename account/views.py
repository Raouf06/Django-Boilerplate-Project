from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from account.models import *
from core.models import *

def registration_view(request):
	context = {}

	if request.user.is_authenticated:
		return redirect('core:index')
	if request.POST:
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(username=username, password=raw_password)
			login(request,account)
			return redirect('core:index')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'register.html', context)

def logout_view(request):
	logout(request)
	return redirect('core:index')

def login_view(request):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect('core:index')
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			try:
				user = authenticate(username=Account.objects.get(email=username),password=password)
			except:
				user = authenticate(username=username,password=password)
			if user:
				login(request,user)
				return redirect('core:index')
	else:
		form = AccountAuthenticationForm()
	context['login_form'] = form
	return render(request,'login.html', context)