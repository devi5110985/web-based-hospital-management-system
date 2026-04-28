from django.shortcuts import render , redirect
from Doctor.models import AddDoctor, Doctor_Medication
from Doctor.forms import AddDoctor_Form , Doctor_Update_form
from django.contrib import messages
from Patient.models import Book_Appointment, Patient_Regiser
from django.core.mail import EmailMessage
from django.conf import settings
from Admin.models import Payment_Model , Pyment_Details
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
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


def Admin_Medication_View(request):
    data = Doctor_Medication.objects.filter(medication='Sended')
    return render(request, 'Admin/Admin_Medication.html', {'data': data})


# ============================================================
# JSON API endpoints for AJAX / charts (consumed by frontend JS)
# ============================================================

def api_admin_stats(request):
    doctors_total = AddDoctor.objects.count()
    patients_total = Patient_Regiser.objects.count()
    appointments_pending = Book_Appointment.objects.filter(status='Pending').count()
    appointments_approved = Book_Appointment.objects.filter(status='Approved').count()
    medications_sent = Doctor_Medication.objects.filter(medication='Sended').count()
    payments_paid = Payment_Model.objects.filter(status='Paid').count()
    payments_due = Pyment_Details.objects.count()

    specializations = {}
    for doc in AddDoctor.objects.all():
        specializations[doc.specialization] = specializations.get(doc.specialization, 0) + 1

    return JsonResponse({
        'doctors': doctors_total,
        'patients': patients_total,
        'pending': appointments_pending,
        'approved': appointments_approved,
        'medications': medications_sent,
        'payments_paid': payments_paid,
        'payments_due': payments_due,
        'specializations': specializations,
    })


def api_doctors_list(request):
    docs = [{
        'id': d.id, 'name': d.name, 'email': d.email, 'phone': d.phone,
        'specialization': d.specialization, 'qualification': d.qualification,
        'experience': d.experience,
    } for d in AddDoctor.objects.all()]
    return JsonResponse({'doctors': docs})


@require_POST
@csrf_exempt
def api_delete_doctor(request, id):
    try:
        AddDoctor.objects.get(id=id).delete()
        return JsonResponse({'ok': True, 'message': 'Doctor deleted successfully'})
    except AddDoctor.DoesNotExist:
        return JsonResponse({'ok': False, 'message': 'Doctor not found'}, status=404)


@require_POST
@csrf_exempt
def api_approve_appointment(request, id):
    try:
        appt = Book_Appointment.objects.get(id=id)
        appt.status = 'Approved'
        appt.save()
        return JsonResponse({'ok': True, 'message': f'Appointment approved for {appt.name}'})
    except Book_Appointment.DoesNotExist:
        return JsonResponse({'ok': False, 'message': 'Appointment not found'}, status=404)


def api_doctor_stats(request):
    doctor_name = request.session.get('doctor_name')
    if not doctor_name:
        return JsonResponse({'error': 'not authenticated'}, status=401)
    try:
        doctor = AddDoctor.objects.get(name=doctor_name)
    except AddDoctor.DoesNotExist:
        return JsonResponse({'error': 'doctor not found'}, status=404)

    my_patients = Book_Appointment.objects.filter(doctor_name=str(doctor), status='Approved').count()
    sent_meds = Doctor_Medication.objects.filter(doctor_name=str(doctor), medication='Sended').count()
    pending_meds = Book_Appointment.objects.filter(doctor_name=str(doctor), status='Approved', medication='None').count()

    return JsonResponse({
        'my_patients': my_patients,
        'sent_medications': sent_meds,
        'pending_medications': pending_meds,
        'doctor_name': doctor.name,
        'specialization': doctor.specialization,
    })


def api_patient_stats(request):
    name = request.session.get('name')
    if not name:
        return JsonResponse({'error': 'not authenticated'}, status=401)

    appts = Book_Appointment.objects.filter(name=name).count()
    approved = Book_Appointment.objects.filter(name=name, status='Approved').count()
    meds = Doctor_Medication.objects.filter(name=name, medication='Sended').count()
    payments = Payment_Model.objects.filter(name=name).count()
    paid = Payment_Model.objects.filter(name=name, status='Paid').count()

    return JsonResponse({
        'name': name,
        'appointments_total': appts,
        'appointments_approved': approved,
        'medications': meds,
        'payments_total': payments,
        'payments_paid': paid,
    })
