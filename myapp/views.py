from django.shortcuts import render,redirect
from .forms import sign_form,notesform,updateform
from .models import Sign_up
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import send_mail
import random
import requests

# Create your views here.
def index(request):
    if request.method == "POST":
        if request.POST.get("signup") == "signup":
            user = sign_form(request.POST)
            if user.is_valid():
                user.save()
                print("Saved!")
                # #Email Sending Code...
                otp = random.randint(1111,9999)
                sub = 'Welcome!'
                msg = f"Dear User!\nYour Account has Been Created With Us!\nEnjoy our Service!\nYour one Time Password:{otp}\nIf Any querry. Contact on\nmatinaibani8@gmail.com | +919510695745"
                from_id = "pythoncs496@gmail.com"
                to_id = [request.POST['username']]
                send_mail(subject=sub,message=msg,from_email=from_id,recipient_list=to_id)
                messages.info(request,"Signup Successfull!")
                return redirect("notes") 
                
            else:
                
                print(user.errors)
                messages.error(request,"Error! Something wen wrong...  Try after Some Time.")
        elif request.POST.get("signin") == "signin":
            unm = request.POST['username']
            pas = request.POST['password']


            user = Sign_up.objects.filter(username=unm,password=pas) 
            uid = Sign_up.objects.get(username=unm)
            # print("Userid :",uid.id)

            if user:
                print("Login Successfully!")
                request.session["user"] = unm #Session Creation
                request.session["uid"] = uid.id
                #Send SMS and OTP
                # otp = random.randint(1111,9999)
                # url = "https://www.fast2sms.com/dev/otp/send"
                
                # headers = {
                #     "Authorization": 'waybXDUnGBoRWspxVejlQMPSvchqkYuit93F2rmTKO67dELN5HQsmH3bLT470hBFapefAl5vInJxSiow',
                #     "Content-Type": "application/json"
                # }
                
                # data = {
                #     "mobile": '9510695745',
                #     "otp_id": f'{otp}',
                #     "otp_length": 4,
                #     "otp_expiry": 10
                # }
                
                # response = requests.post(
                #     url,
                #     headers=headers,
                #     json=data
                # )
                # print(response.status_code)
                # print(response.json())
                return redirect('notes')
            else:
                print("Error!")
                messages.error(request,"Error! Username and Password does Not Match!")

    return render(request,"index.html")

def notes(request):
    user = request.session.get('user')
    if request.method == "POST":
        mynotes = notesform(request.POST,request.FILES)
        if mynotes.is_valid():
            mynotes.save()
            print("Saved!")
        else:
            print(mynotes.errors)

    return render(request,"notes.html",{'cuser':user})

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def profile(request):
    user = request.session.get('user')
    uid = request.session.get('uid')
    cid = Sign_up.objects.get(id=uid)
    if request.method == "POST":
        user = updateform(request.POST)
        if user.is_valid():
            update = updateform(request.POST,instance=cid)
            update.save()
            print("Profile Updated!")
            return redirect("notes")
        else:
            print(user.errors)
    return render(request,"profile.html",{'cuser':user,'uid':Sign_up.objects.get(id=uid)})

def userlogout(request):
    logout(request)
    return redirect("/")