from django import forms

from Doctor.models import AddDoctor

class AddDoctor_Form(forms.ModelForm):

    name= forms.CharField(widget=(forms.TextInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), required=True ,  max_length=100)

    specialization = forms.CharField(widget=(forms.TextInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), required=True ,  max_length=100)

    email = forms.EmailField(widget=(forms.EmailInput( attrs={'class': 'form-control' ,'autocomplete': 'off'})),required=True, max_length=100)

    phone = forms.CharField(widget=(forms.TextInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})),required=True, max_length=10)

    qualification = forms.CharField(widget=(forms.TextInput( attrs={'class': 'form-control'  , 'autocomplete': 'off'})), required=True , max_length=100)
    experience = forms.IntegerField(widget=(forms.NumberInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), required=True)
    password = forms.CharField(widget=(forms.PasswordInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), required=True ,  max_length=100)

    confirm_Password = forms.CharField(widget=(forms.PasswordInput( attrs={'class': 'form-control' , 'autocomplete': 'off'})), required=True, max_length=100)


    class Meta: 
        model = AddDoctor
        fields = '__all__'



class Doctor_Update_form(forms.ModelForm):
    class Meta:
        model = AddDoctor
        fields = ['name','email','phone','specialization','qualification','experience']