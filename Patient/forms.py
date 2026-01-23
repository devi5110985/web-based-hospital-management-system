from django import forms
from Patient.models import Patient_Regiser ,Book_Appointment 
from Doctor.models import AddDoctor

class Patient_Regiser_Form(forms.ModelForm):
    name = forms.CharField( widget=(forms.TextInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), required=True ,  max_length=100)
    email = forms.EmailField( widget=(forms.EmailInput( attrs={'class': 'form-control' ,'autocomplete': 'off'})),required=True, max_length=100)
    phone = forms.CharField(widget=(forms.TextInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})),required=True, max_length=10)
    password = forms.CharField(widget=(forms.PasswordInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), required=True , max_length=100)
    confirm_password = forms.CharField(widget=(forms.PasswordInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), required=True , max_length=100)
    class Meta:
        model = Patient_Regiser
        fields = '__all__'


class Book_Appointment_Form(forms.ModelForm):
    
   
     name   =  forms.CharField( 
         widget=(forms.TextInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})),
         required=True ,  max_length=100)
   
     phone   =  forms.CharField(
         widget=(forms.TextInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})),
         required=True, max_length=10)
   
     age     = forms.IntegerField(
         widget=(forms.NumberInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), 
         required=True)
   
     address = forms.CharField( 
         widget=(forms.TextInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), 
         required=True ,  max_length=100)
   
     problem  = forms.ChoiceField(
         choices=[('','select conservative department')]+[(option, option) for option  in AddDoctor.objects.values_list('specialization', flat=True).distinct()],
         required=True,
         widget=forms.Select(attrs={'class': 'form-control'}))
     
     upload_report = forms.FileField(
        widget=(forms.FileInput( attrs={'class': 'form-control' , 'autocomplete': 'off' , 'accept':'pdf'})),required=True
    )
   
     doctor_name  = forms.ModelChoiceField(
        queryset=AddDoctor.objects.all(),
        empty_label='Select doctor',
        widget=forms.Select(attrs={'class': 'form-control'}))
   
        # Define the widget correctly
     medication = forms.CharField(
         widget=(forms.HiddenInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), required=True , initial='None' , max_length=100
     )
    
     status = forms.CharField( 
         widget=(forms.HiddenInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})),
           required=True , initial='Pending', max_length=100)
     class Meta:
        model =Book_Appointment
        fields = '__all__'


        def __init__(self, *args, **kwargs):
            super(Book_Appointment_Form, self).__init__(*args, **kwargs)
            self.fields['doctor_name'].label_from_instance = lambda obj: f"{obj.name} - {obj.specialization}"




