from django.urls import path
from Doctor import views

urlpatterns = [
    path('Doctor_Login/',views.Doctor_Login , name="Doctor_Login"),
    path('Doctor_Home_page/',views.Doctor_Home_page , name="Doctor_Home_page"),
    path('Show_Patients/',views.Show_Patients , name="Show_Patients"),
    path('Medication/<int:id>',views.Medication , name="Medication"),
    path('Medication_view_admin/' , views.Medicatin_view_admin , name='Medication_view_admin')
]