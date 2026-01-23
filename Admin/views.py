from django.shortcuts import render , redirect
from Doctor.models import AddDoctor
from Doctor.forms import AddDoctor_Form , Doctor_Update_form
from django.contrib import messages
from Patient.models import Book_Appointment 
from django.core.mail import EmailMessage
from django.conf import settings
from Admin.models import Payment_Model , Pyment_Details
# Create your views here.
def Base(request):
    return render(request,'base.html')

#############################################################################################################

def Admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(username , password)
        if username == 'admin' and password == 'admin':
            return redirect('Admin_Home')
    return render(request,'Admin_lgoin.html')

#############################################################################################################

def Admin_Home(request):
    return render(request,'Admin/AdminHome.html')


#############################################################################################################

# def Email_sending():
#     user = AddDoctor.objects.all()

#     for i in user:
#         print(i.email)

def Add_Doctor(request):
    if request.method == 'POST':
        try:
          if  AddDoctor.objects.filter(email = request.POST['email']).exists():
             messages.error(request, 'Email already exists')
          elif request.POST['password'] != request.POST['confirm_Password']:
               messages.error(request, 'Passwords and confirm passwords must be same')    
          else:
               form = AddDoctor_Form(request.POST)
               if form.is_valid():
                  form.save()
                  messages.success(request, 'Doctor added successfully')
                  email = request.POST.get('email')
                  Email_body = f" Hello  Doctor\n your username :- {request.POST.get('name')} \n your password :- {request.POST.get('password')}\n  please login to your account\n This id and Password is totally Contidential Please don't share this Id and Password to anyone\n This mail is a Computer Generated mail please do not reply \n Thanks"  
                  Email_message = EmailMessage(subject = 'Doctor Registration', body = Email_body, to = [email] , from_email = settings.EMAIL_HOST_USER)
                  Email_message.fail_silently = True
                  Email_message.send()
                  messages.success(request  , 'Email sent successfully')
                  return redirect('Add_Doctor')
               else:
                  messages.error(request, 'Error adding doctor')
        except Exception as e:
           messages.error(request, f'Error adding doctor: {str(e)}')          
    
    form = AddDoctor_Form()            
    return render(request,'Admin/Add_Doctor.html' , {'form':form})


#########################################################################################################

def Doctor_Details(request):
    Doctor_data = AddDoctor.objects.all()
    return render(request,'Admin/Doctor_Details.html' , {'Doctor_data':Doctor_data})


###########################################################################################################

def Update_Doctor_Details(request , id):
    form = AddDoctor.objects.get(id = id)
    if request.method == 'POST':
        form = Doctor_Update_form(request.POST , instance = form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor  Recored updated successfully')
            return redirect('Doctor_Details')
        else:
            messages.error(request, 'Error updating doctor')
    form = Doctor_Update_form(instance = form)
    return render(request,'Admin/Update_Doctor_Details.html' , {'form':form})

#####################################################################################################################

def Delete_Doctor_details(request , id):
    AddDoctor.objects.get(id = id).delete()
    messages.success(request, 'Doctor Reocord deleted successfully')
    return redirect('Doctor_Details')




def View_Appointmets(request):
    appointment = Book_Appointment.objects.filter(status='Pending')

    return render(request,'Admin/View_Appointments.html' , {'appointment':appointment})




def Aprove_Appointments(request , id):
    appointment = Book_Appointment.objects.get(id = id)
    appointment.status = 'Approved'
    appointment.save()
    messages.success(request, f' {appointment.name} Your Appointment Sucessfylly forword to Doctor {appointment.doctor_name}' )
    return redirect('View_Appointments')





def All_Patient_information(request):
    Patient_data = Book_Appointment.objects.all()
    
    return render(request,'Admin/All_Patient_information.html' , {'Patient_data':Patient_data})

def View_Patient_Payments(request, id ):
    Patient_data = Book_Appointment.objects.get(id = id)
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        if name and amount:
         Pyment_Details.objects.create(name=name,amount=amount)
         messages.success(request, 'Payment added successfully')
    return render(request,'Admin/View_patient_payments.html', {'Patient_data':Patient_data}) 


                                                                                     