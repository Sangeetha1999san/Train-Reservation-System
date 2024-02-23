from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from RegistrationModule.models import LoginDetails
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def login_view(request):
	c={}
	c.update(csrf(request))
	return render(request,'loginPage.html',c)

def auth_login(request):
	username=request.POST.get('username','')
	password=request.POST.get('password','')

	c={}
	c.update(csrf(request))
	try:
		user=LoginDetails.objects.get(username=username)
	except ObjectDoesNotExist:
		msg="INVALID CREDENTIAL....      PLEASE TRY AGAIN..."
		c.update({"errorMsg":msg})		
		return render(request,'invalidLogin.html',c)	
	else:
		if user is not None and user.password==password:
			request.session['username']=username
			return HttpResponseRedirect('/bookTicket/homePage/',c)
		else:
			msg="INVALID CREDENTIAL....      PLEASE TRY AGAIN..."
			c.update({"errorMsg":msg})		
			return render(request,'invalidLogin.html',c)	
