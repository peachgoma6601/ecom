from django import forms

from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'confirm password',
    }))    


    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
            ]

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password =cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password does not Match !!')        


    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter your name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter your name'
        self.fields['email'].widget.attrs['placeholder']='Enter your name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter your name'

        for filed in self.fields:
            self.fields[filed].widget.attrs['class']='form-control'

