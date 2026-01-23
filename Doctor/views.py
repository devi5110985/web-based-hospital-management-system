from django.shortcuts import render , redirect
from Patient.models import *
from Doctor.models import *
from django.contrib import messages
# Create your views here.



def Doctor_Login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['pws']
        try:
            if username and password:
                doctor = AddDoctor.objects.get(name = username , password = password)
                if doctor:
                    request.session['doctor'] = username
                    request.session['doctor_id'] = doctor.id
                    request.session['doctor_name'] = doctor.name
                    print( 'Login successfully')
                    return redirect('Doctor_Home_page')
                else:
                    messages.error(request , 'Invalid username or password')
            else:
                messages.error(request , 'Please enter username and password')
        except Exception as e:
            messages.error(request , f'Error logging in: {str(e)}')

    return render(request,'Doctor/Doctor_login.html')



def Doctor_Home_page(request):
    return render(request , 'Doctor/Doctor_Home.html')




def Show_Patients(request):
    # Get the doctor object based on the session value
    doctor = AddDoctor.objects.get(name=request.session['doctor_name'])
    
    # Filter the appointments to match the doctor and the approved status
    Patient_data = Book_Appointment.objects.filter(doctor_name=doctor, status='Approved' , medication='None')
    
    # Render the template with the filtered data
    return render(request, 'Doctor/Show_Patients.html', {'Patient_data': Patient_data})



def Medication(request , id):
    form = Book_Appointment.objects.get(id = id)
    if request.method == 'POST':
        name = request.POST.get('name')
        doctor_name = request.POST.get('doctor_name')
        prescription = request.POST.get('prescription')
        admitted = request.POST.get('admit')
        medication_status = request.POST.get('medication')
        print(f'{name} {doctor_name} {prescription} {admitted}{medication_status}')
        if name and doctor_name and prescription and admitted and medication_status:
            Doc_Med = Doctor_Medication.objects.create(name=name, doctor_name=doctor_name, prescription=prescription,
                                                        admitted=admitted , medication=medication_status)
            messages.success(request, 'Medication sended successfully' )
            Doc_Med.save()
            Book_Appointment.objects.filter( id=id , name=name).update(medication='Sended')
            Doctor_Medication.objects.filter(name=name).update(medication='Sended')

            return redirect('Show_Patients')
            
            
    return render(request,'Doctor/Medication.html' , {'form':form})



def Medicatin_view_admin(request):
    data = Doctor_Medication.objects.filter(medication='Sended')
    print('axsasasas',data)

    return render(request  ,'Doctor/Medicatin_view_admin.html'  , {'data':data})