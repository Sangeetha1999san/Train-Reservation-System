from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from RegistrationModule.models import UserDetails,LoginDetails
import re
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def registration_view(request):
	c={}
	c.update(csrf(request))
	return render(request,'registration.html',c)


def auth_registration(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    confpass = request.POST.get('confpass', '')
    fname = request.POST.get('firstname', '')
    lname = request.POST.get('lastname', '')
    gender = request.POST.get('gender', '')
    dob = request.POST.get('dateofbirth', '')
    cno = request.POST.get('contactnumber', '')
    email = request.POST.get('emailid', '')

    isValid = True
    msg = ""

    # Username validation
    if len(username) < 6 or len(username) > 10:
        isValid = False
        msg = "Username should be of length 6-10"

    # Password validation
    if len(password) < 10:
        isValid = False
        msg = "Password must be at least 10 characters long."
    elif not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@#$%&!])[A-Za-z\d@#$%&!]+$', password):
        isValid = False
        msg = "Password should be a combination of letters, digits, and special characters."

    if password != confpass:
        isValid = False
        msg = "Password & Confirm password must be the same."

    # Contact number validation
    RegexForContactNumber = r'[0-9]{10}'
    pattern = re.compile(RegexForContactNumber)
    if not re.match(pattern, cno):
        isValid = False
        msg = "Please enter a valid contact number."

    # Email validation
    RegexForEmail = r'\S+@([a-z]+)((\.([a-z]+))+)'    
    pattern = re.compile(RegexForEmail)
    if not re.match(pattern, email):
        isValid = False
        msg = "Please enter a valid email id."

    c = {}
    c.update(csrf(request))

    if isValid:
        try:
            user = UserDetails.objects.get(username=username)
        except ObjectDoesNotExist:
            l = LoginDetails(username=username, password=password)
            u = UserDetails(username=username, password=password, f_name=fname, l_name=lname, gender=gender,
                            dob=dob, contact_number=cno, email=email)
            u.save()
            l.save()
            return HttpResponseRedirect('/loginModule/loginPage/', c)
        else:
            msg = "This Username already exists. Please try with a different username."
            c.update({"errorMsg": msg})
            return render(request, 'invalidRegistration.html', c)
    else:
        c.update({"errorMsg": msg})
        return render(request, 'invalidRegistration.html', c)

