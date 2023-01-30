import requests
import json
from django.shortcuts import redirect, render
import json
from .models import*
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.contrib.auth.decorators import login_required


def dummy(request):
    city = City.objects.all()
    role = Role.objects.all()
    return render(request,'dummy.html',{'city':city,'role':role})

def register(request):
    
    demo3 = ""
    city_search=""
    city_name = ""
    role = Role.objects.all()
    city = City.objects.all()
    if request.method == "POST":
        role3 = request.POST.get('testing')
        city_search = request.POST.get('city_search')
        cityy = City.objects.get(id=role3)
        role2 = Role.objects.filter(city_id=cityy)
        demo3 = role2
        city_name = City.objects.get(id=city_search)
        
        
    return render(request,'MEMBERS/register.html',{'role':role,'city':city,'demo':demo3,'city_name':city_name})



def douserregister(request):
   
    pic = Member.objects.all()

    if request.method == "POST":

        role_id = request.POST.get("role_id")
        role_id2 = request.POST.get("role_id2")

        username = request.POST.get("username")
        father_name = request.POST.get("father_name")
        gender = request.POST.get("gender")
        mobile_no = request.POST.get("mobile_no")
        dob = request.POST.get("dob")
        adhaar = request.POST.get("adhaar")
        pan_no = request.POST.get("pan_no")
        caste = request.POST.get("caste")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pin = request.POST.get("pin")
        address = request.POST.get("address")
        marital_status = request.POST.get("marital_status")
        job_seeker = request.POST.get("job_seeker")
        adhar_front = request.FILES.get('adhar_front')
        adhar_back = request.FILES.get('adhar_back')
        profile_pic = request.FILES.get('photo')
        print("profile",profile_pic)

        
        
        password = request.POST.get('dob')
       

        role=Role.objects.get(id=role_id)
       

        

        amount = int(request.POST.get("amount"))*100 
        client=razorpay.Client(auth =("rzp_test_czVP739sBN5blU" , "MBpgYsg92tAkraZtv5BMyLeq"))
        
        payment=client.order.create({'amount':amount, 'currency':'INR' , 'payment_capture' : '1'})
        user=CustomUser.objects.create_user(username=username,adhaar=adhaar,password=password,user_type=4)
        user.member.father_name=father_name
        user.member.gender=gender
        user.member.mobile_no=mobile_no
        user.member.dob=dob
        user.member.adhaar=adhaar
        user.member.pan_no=pan_no
        user.member.caste=caste
        user.member.city=city
        user.member.state=state
        user.member.pin=pin
        user.member.marital_status=marital_status
        user.member.job_seeker=job_seeker
        # user.member.email=email
        user.member.address=address
        user.member.adhar_front=adhar_front
        user.member.adhar_back=adhar_back
        user.member.profile_pic=profile_pic

        user.member.role_id=role
        
        user.member.amount=amount
        user.member.payment_id=payment['id']
        # if user.member.paid == True:
        user.save()

    #   
        context = {
            
        'username':username,
        # 'father_name':father_name,
        'mobile_no':mobile_no,
        'adhaar':adhaar,     
        'profile_pic':profile_pic,     
        'payment':payment,
        'dob':dob,
        'pic':pic

        }

        return render(request , 'homepage/doregister.html',context)
    return render(request,'homepage/doregister.html')
        
    
@csrf_exempt
def Success(request):
 if request.method=="POST":
     a=request.POST
     print(a)
     order_id=""
     for key,val in a.items():
      if key=="razorpay_order_id":
        order_id = val
        break
     user=Member.objects.filter(payment_id=order_id).first() 
     user.paid=True
     user.save()
 return render(request , 'MEMBERS/success.html')   




def member_login(request):
    return render(request,'MEMBERS/login2.html')



def doLogin(request):
    
        user=EmailBackEnd.authenticate(request,username=request.POST.get("adhaarNo"),password=request.POST.get("password"))
        print("oooo",user)
        
        if user!=None:
            print("hello")
            login(request,user)
            if user.user_type=="4":
                return HttpResponseRedirect(reverse("member_dashboard"))
           
        else:
            messages.error(request,"Invalid adhaar number or password !!")
            return redirect("member_login")
            # return HttpResponseRedirect(reverse("member_login"))


# @login_required(login_url='member_login')


def dashboard(request):
    user = request.user
    member = Member.objects.filter(admin=user)
    
    return render(request,'MEMBERS/dashboard.html',{'member':member})

def payment_information(request):
    

    member = Member.objects.filter(admin=request.user)
    return render(request,'MEMBERS/payment_info.html',{'member':member})


def member_profile(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
       
        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "Your Profile Updated Successfully !!")
            return HttpResponseRedirect(reverse("member_profile"))
            # redirect('/')
            
            
        except :
            messages.error(request, "Failed to Update Your Profile")
    return render(request,'MEMBERS/profile.html')  


def member_list(request):
    return render(request, 'MEMBERS/list.html')  