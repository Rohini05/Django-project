from django.shortcuts import render
from .models import User_Application_Detail,admin_details                     
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Q
from rest_framework import viewsets
from .serializers import applicationInfoSerializer
from rest_framework.permissions import IsAuthenticated
import csv
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

def view_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            
            login(request,user)
            messages.success(request, 'Login Successful')
            
            return redirect('ApplicationListview')
        else:
            messages.error(request,'Invalid credentials, Please check email/phone or password. ')
            return render(request, 'electricity_mgmt/login.html')
    else:
        print("in last else")
        return render(request, 'electricity_mgmt/login.html')

    
def register(request):
    
    if request.method       == 'POST':
        username            = request.POST['username']
        email               = request.POST['email']
        password1           = request.POST['password1']
        password2           = request.POST['password2']
       
        if password1==password2:
            if admin_details.objects.filter(email=email).exists():
                messages.info(request, 'email Taken')
                return redirect('register')
            else:
                user = admin_details.objects.create_user(name=username, password=password1, email=email,is_active=True)
                user.set_password(password1)            
                user.save()
               
        else:
            messages.info(request, 'password not matched')
            return redirect('register')

        return redirect('register')


    else:
        return render(request, 'electricity_mgmt/register.html')

def createApplication(request):
    # personal_info = Personal_Info.objects.all()
    # ui = MyUser.objects.get(pk=id)
    if request.method == 'POST':
        
        applicant_name = request.POST['applicant_name']
        mail_id = request.POST['mail_id']
        gender = request.POST['gender']
        district = request.POST['district']
        state = request.POST['state']
        pincode = request.POST['pincode']
        ownership = request.POST['ownership']
        gov_id_type = request.POST['gov_id']
        id_num = request.POST['id_num']
        category = request.POST['category']
        load_Apply_kv = request.POST['load_kv']
        
        # sms_notification_active  = request.POST['sms_notification_active']
        # email_notification_active  = request.POST['email_notification_active']


        

        pi = User_Application_Detail.objects.create(applicant_name=applicant_name, gender=gender, mail_id=mail_id, 
                         district=district, id_num=id_num, pincode=pincode, 
                        ownership=ownership, gov_id_type=gov_id_type, state=state, category=category, load_Apply_kv=load_Apply_kv)
        pi.save()
        print(pi)
        return render(request,'electricity_mgmt/form.html',context={"msg":200})   
    else:
        return render(request, 'electricity_mgmt/form.html')

    

@login_required
def ApplicationListview(request):  #ListView for all Model or Table at profile page

    if 'q' in request.GET:
        q = request.GET['q']
        # data = Data.objects.filter(last_name__icontains=q)
        multiple_q = Q(Q(applicant_name__icontains=q) | Q(state__icontains=q)| Q(id__icontains=q))
        applicant_details = User_Application_Detail.objects.filter(multiple_q)
    else:
        applicant_details = User_Application_Detail.objects.all()
        q=''

    context = {'applicant_details':applicant_details,"user":request.user,'q':q}

    return render(request, 'electricity_mgmt/table.html', context)






@login_required
def updateApplication(request,id):
    # pi = Personal_Info.objects.get(id=id)   

    if request.method == 'POST':
        # cur_user = request.user.pi
        
        print(request.user)
        # user_id = current_user.id
    
        app=User_Application_Detail.objects.get(id=id)
        status = request.POST['status']
        reviewer_comments = request.POST['comment']

        app.status = status
        app.reviewer_comments = reviewer_comments
        app.reviewer_id=request.user
        if status =='Approved':
            app.date_of_approved =datetime.datetime.now()
        app.modified_date=datetime.datetime.now()
        # pi.display_contact_number = display_contact_number          
        app.save()    
        return redirect('ApplicationListview')
    else:
        return render(request, 'ApplicationListview')




def user_logout(request):
    logout(request)
    print('logout done')
    messages.success(request, 'Account logout successfully')
    return redirect('login')




########### API ################
class createPrivateInfo(viewsets.ModelViewSet):
    queryset = User_Application_Detail.objects.all()
    serializer_class = applicationInfoSerializer
    permission_classes = (IsAuthenticated,)

   #------- list is used to increase resume count ----#
    def list(self, request):
        response = {'message': 'list function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
