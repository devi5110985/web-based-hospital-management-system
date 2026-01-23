from django.urls import path
from Patient import views
urlpatterns = [
    path('',views.Patinet_Register_View , name="Patient_Register"),
    path('Book_Appointments/',views.Book_Appointment_View , name="Book_Appointments"),
    path('Patient_Login/',views.Patient_Login_View , name="Patient_Login"),
    path('Patient_Home/' , views.Patient_Home , name="Patient_Home"),
    path('Reports/' , views.Medication_Reoprt , name="Reports"),
    path('Download_report/' , views.Report_pdf_view , name="download_report"),
    path('Payment/' , views.Paytment_view , name="Payment"),
    

  
]