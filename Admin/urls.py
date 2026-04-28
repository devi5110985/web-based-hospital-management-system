from django.urls import path
from Admin import views

urlpatterns = [

    path('',views.Base , name="base"),
    path('Admin_login/',views.Admin_login , name="Admin_login"),
    path('Admin_Home/',views.Admin_Home , name="Admin_Home"),
    path('Add_Doctor/',views.Add_Doctor , name="Add_Doctor"),
    path('Doctor_Details/',views.Doctor_Details , name="Doctor_Details"),
    path('Update_Doctor_Details/<int:id>/',views.Update_Doctor_Details , name="Update_Doctor_Details"),
    path('Delete_Doctor_Details/<int:id>/',views.Delete_Doctor_details , name="Delete_Doctor_Details"),
    path('View_Appointments/',views.View_Appointmets , name="View_Appointments"),
    path('Add_Appointments/<int:id>/',views.Aprove_Appointments , name="Add_Appointments"),
    path('All_Patient_information/',views.All_Patient_information , name="All_Patient_information"),
    path('View_patient_payments/<int:id>/',views.View_Patient_Payments , name="View_patient_payments"),
    path('Admin_Medication/',views.Admin_Medication_View , name="Admin_Medication"),

    # JSON APIs (consumed by frontend JS — Chart.js, fetch, HTMX)
    path('api/admin/stats/', views.api_admin_stats, name='api_admin_stats'),
    path('api/doctors/', views.api_doctors_list, name='api_doctors_list'),
    path('api/doctor/<int:id>/delete/', views.api_delete_doctor, name='api_delete_doctor'),
    path('api/appointment/<int:id>/approve/', views.api_approve_appointment, name='api_approve_appointment'),
    path('api/doctor/stats/', views.api_doctor_stats, name='api_doctor_stats'),
    path('api/patient/stats/', views.api_patient_stats, name='api_patient_stats'),
]