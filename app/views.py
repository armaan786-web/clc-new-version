import json
from django.shortcuts import redirect, render
import requests
import razorpay
from .models import*
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator





# Create your views here.
def home(request):
    course = Course.objects.all()
    job = Job.objects.all().order_by('id')[0:5]

    return render(request,'homepage/home.html',{'job':job,'course':course})

def joblisting(request):

    contact_list = Job.objects.all().order_by('-id')
    paginator = Paginator(contact_list, 2) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # print("page number",page_obj)
    # return render(request, 'list.html', {'page_obj': page_obj})
    return render(request,'homepage/job_listing.html',{'page_obj':page_obj})


def jobdetails(request,pk):
    
    job=Job.objects.all().filter(id=pk)

    return render(request,'homepage/job_details.html',{'job':job})

def course(request):
    
    course = Course.objects.all().order_by('-id')
    paginator = Paginator(course, 2) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'homepage/course.html',{'course':page_obj})



def about(request):
     return render(request,'homepage/about.html')

def contact(request):
     return render(request,'homepage/contact.html')
     
def contact(request):
     return render(request,'homepage/contact.html')

def profile(request):
     if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # print(first_name)
        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "Your Profile Updated Successfully !!")
            return HttpResponseRedirect(reverse("profile"))
            # redirect('/')
            
            
        except :
            messages.error(request, "Failed to Update Your Profile")
     return render(request,'homepage/profile.html')
     
@login_required(login_url='member_login')
def apply(request):
     return render(request,'homepage/apply.html')

def gallery(request):
     return render(request,'homepage/gallery.html')

def manage_gallery(request):
     return render(request,'HOD/manage_gallery.html')

def add_gallery(request):
    if request.method == "POST":
        print("hello")
        galary = request.FILES.get('profile_pic')
        print(galary)

    return render(request,'HOD/add_gallery.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url="/EMPLOYERS/login2")
def success(request):
    return render(request,'success.html')


def worlker_list(request,id):
    # Employer_id = request.user
    # print("EEEEEEEEE",Employer_id)
    role = Role.objects.get(id=id)
    mem = Member.objects.filter(role_id = role).order_by('?')[:3]
    emp_gov=Employer.objects.get(admin=request.user.id)
    monthly = Booking.objects.get(employer_id__admin = request.user.id)
    total = monthly.total_monthly
    total_price = total*100
    
  
   
    booking=Employer.objects.get(admin=request.user.id)
    book = Booking.objects.get(employer_id=booking)
    

    
    
    member = Member.objects.filter(role_id_id=id)
    
   

    # if request.method == "POST":
        
    #     title = request.POST.get('amt')
    #     print("helloooooooo",title)
        # return HttpResponse(status=204,headers={
        #     'HX-Trigger': json.dumps({
        #                 "movieListChanged": None,
        #                 "showMessage": f"added."
                        
        #             })
        # })
        
        
    
    
    return render(request,'demo.html',{'member':member,'booking':booking,'mem':mem,'emp_gov':emp_gov,'monthly':monthly,'total_price':total_price,'book':book})    
    # return render(request,'demo.html')    


   
@csrf_exempt
def booking_Success(request):
    if request.method=="POST":
        a=request.POST
        print(a)
        order_id=""
        for key,val in a.items():
            if key=="razorpay_order_id":
                order_id = val
                break
        user=Booking.objects.filter(payment_id=order_id).first() 
        user.paid=True
        user.save()
    return render(request , 'MEMBERS/success.html')   

def worker_role_view(request,leave_id):
    leave=Member.objects.get(id=leave_id)
    leave.status=1
    leave.save()
    return redirect('employer_managebooking')
    # return HttpResponseRedirect(reverse("worlker_list"))

def testing(request):
    event_list = Role.objects.all()
    if request.method == "POST":
        id_list = request.POST.getlist('boxes')
        # print(id_list)
        event_list.update(is_employer=False)
        for x in id_list:
            Role.objects.filter(id= int(x)).update(is_employer=True)
    return render(request,'testing.html',{'event_list':event_list})