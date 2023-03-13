from django import forms  
from .models import Account,UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
  
   password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
   confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
   class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        
        }
   def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(str(e))
        confirm_password=cleaned_data.get('confirm_password')
        if password!=confirm_password:
          raise forms.ValidationError(
             "Password does not match!"   
           )
         
   def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form_control'
        
        

class UserForm(forms.ModelForm):
     # class Meta:
     #      model=Account
     #      fields=('first_name','last_name','phone_number')
          
     # def __init__(self,*args,**kwargs):
     #    super(UserForm,self).__init__(*args,**kwargs)   
     #    for field  in self.fields:
     #         self.fields[field].widget.attrs['class']='form-control'    
      class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': ' First Name','class' : 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name','class' : 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number','class' : 'form-control'}),
                
        }  
          
class UserProfileForm(forms.ModelForm):
     profile_picture=forms.ImageField(required=False,error_messages={'invalid':("image files only")},widget=forms.FileInput)
     class Meta:
          model=UserProfile
          fields=('address_line_1','address_line_2','city','state','country','profile_picture','zip_code')       
          widgets = {
            'address_line_1': forms.TextInput(attrs={'placeholder': ' Address_line_1','class' : 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Address_line_2','class' : 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'city','class' : 'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': ' State','class' : 'form-control'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country','class' : 'form-control'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip_code','class' : 'form-control'}),
                
        }       
      
     def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)   
        for field  in self.fields:
             self.fields[field].widget.attrs['class']='form-control'
      
       