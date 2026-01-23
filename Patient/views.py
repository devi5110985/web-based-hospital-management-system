from django.shortcuts import render , redirect
from Patient.models import Patient_Regiser,Book_Appointment
from Patient.forms import Patient_Regiser_Form , Book_Appointment_Form
from django.contrib import messages
from Doctor.models import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import random
from Admin.models import Payment_Model , Pyment_Details
# Create your views here.

def Patinet_Register_View(request):
    if request.method == 'POST':
        try:
            if Patient_Regiser.objects.filter(email = request.POST['email']).exists():
                messages.error(request, 'Email already exists')
            elif request.POST['password'] != request.POST['confirm_password']:
                messages.error(request, 'Passwords and confirm passwords must be same')
            else:
                form = Patient_Regiser_Form(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Patient Record added successfully')
                    return redirect('Patient_Login')
                else:
                    messages.error(request, 'Error adding patient details')
        except Exception as e:
            messages.error(request, f'Error adding patient{str(e)}')
        form = Patient_Regiser_Form(request.POST)
        
    form = Patient_Regiser_Form()
    return render(request,'patient/patient_register.html' , {'form':form})
###############################################################################################################
def Patient_Login_View(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['pws']
        
        try:
            data= Patient_Regiser.objects.filter(name = username , password = password)
            if data:
                request.session['name'] = username
                request.session['id'] = data[0].id
                return redirect('Patient_Home')
            else:
                messages.error(request, 'Invalid username or password')
        except  Exception as e:
            messages.error(request, f'Error logging in: {str(e)}')

     
    return render(request,'patient/patient_login.html')


#################################################################################################################
def Book_Appointment_View(request):
    name = request.session.get('name')
    print(name)

    if request.method == 'POST':
        
        App_form = Book_Appointment_Form(request.POST , request.FILES)
        print('afafafa' , request.POST)
        print('afafafaaaa' , request.FILES)
        try:
            if App_form.is_valid():
                        upload_files = App_form.cleaned_data['upload_report']
                       
                        if upload_files and not upload_files.name.endswith('.pdf') :
                             messages.error(request, 'Only PDF files are allowed')
                             return redirect('Book_Appointments')
                     
                        else:
                            App_form.save()
                            messages.success(request, 'Appointment booked successfully and Please Login for Furthuer Process ')
                            return redirect('Book_Appointments')
            else:
              messages.success(request, 'Error booking appointment')
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')

    App_form = Book_Appointment_Form()

    return render(request,'patient/Book_Appointment.html' , {'App_form':App_form})



#################################################################################################################




#####################################################################################################################

def Patient_Home(request):
    return render(request,'patient/patient_home.html')



def Medication_Reoprt(request):
    

    
    try:
        name =request.session['name']
        data = Doctor_Medication.objects.get(name = name , medication = 'Sended')
        data1 =  Book_Appointment.objects.get(name = name , medication = 'Sended')
    
        return render(request,'patient/Reports.html' , {'data':data , 'data1':data1})
    except Exception as e :
         print(e)
         messages.error(request, "No Medication Avaliable for this patient. Not yet Booked an Appointment")
    return render(request,'patient/Reports.html')


def Paytment_view(request):
      name =request.session['name']
      data = Pyment_Details.objects.get(name=name)
      amount = data.amount
    
      if request.method == 'POST':
        name =request.POST.get('patient_name')
        amount = request.POST.get('amount')
        cardnumber = request.POST.get('cardnumber')
        cardholdername = request.POST.get('cardholdername')
        cvv = request.POST.get('cvv')
        expdate = request.POST.get('expdate')
        status = request.POST.get('status')
        if name and amount and status:
            Paymen = Payment_Model(name= name , amount=amount,status=status)
            Paymen.save()
        if Payment_Model.objects.filter(name = name ).update(status='Paid'):
            messages.success(request, 'Payment Sucessfull')
            return redirect('download_report')
        else:
            messages.error(request, 'Payment Failed')

      return render(request,'patient/Payment.html' , {'name':name , 'amount':amount })
      
 
def Report_pdf_view(request):
    name =request.session['name']
    data = Doctor_Medication.objects.get(name = name , medication = 'Sended')
    data1 =  Book_Appointment.objects.get(name = name , medication = 'Sended')
    

    template_path = 'patient/pdf_report.html'
    context = {'data':data , 'data1':data1 }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{name}_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


