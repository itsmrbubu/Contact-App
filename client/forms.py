from django import forms
from .models import Client, Contact , Message

# Register clients class
class ClientRegisterForm (forms.ModelForm):
    client_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= Client
        fields = {"client_username","client_password","client_avatar","client_email","client_tel"}
        
    def __init__(self, *args, **kwargs):
        super(ClientRegisterForm, self).__init__(*args,**kwargs)
        
        #Adding CSS classes to the django form
        self.fields['client_username'].widget.attrs.update({'class':'form-control'})
        self.fields['client_password'].widget.attrs.update({'class':'form-control'})
        self.fields['client_avatar'].widget.attrs.update({'class':'form-control'})
        self.fields['client_email'].widget.attrs.update({'class':'form-control'})
        self.fields['client_tel'].widget.attrs.update({'class':'form-control'})
        

#Login clients class

class ClientLoginForm (forms.ModelForm):
    client_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= Client
        fields = {"client_username","client_password"}
        
    def __init__(self, *args, **kwargs):
        super(ClientLoginForm, self).__init__(*args,**kwargs)
        
        #Adding css class to the django form
        self.fields['client_username'].widget.attrs.update({'class':'form-control'})
        self.fields['client_password'].widget.attrs.update({'class':'form-control'})
      
        

#Edit Client form

class ClientEditForm (forms.ModelForm):
    client_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= Client
        fields = {"client_username","client_password","client_avatar","client_email","client_tel"}
        
    def __init__(self, *args, **kwargs):
        super(ClientEditForm, self).__init__(*args,**kwargs)
        
        #Adding CSS classes to the django form
        self.fields['client_username'].widget.attrs.update({'class':'form-control'})
        self.fields['client_password'].widget.attrs.update({'class':'form-control'})
        self.fields['client_avatar'].widget.attrs.update({'class':'form-control'})
        self.fields['client_email'].widget.attrs.update({'class':'form-control'})
        self.fields['client_tel'].widget.attrs.update({'class':'form-control'})
       
###################### CONTACT SECTION #################

#create contact form
class CreateContactForm(forms.ModelForm):
    class Meta:
        model = Contact 
        fields = {"contact_with","contact_username","contact_avatar","contact_email", "contact_tel", "client"}
        #Hiding id of logged in client
        widgets = {"client":forms.HiddenInput()}
    
    def __init__(self, *args, **kwargs):
        super(CreateContactForm, self).__init__(*args,**kwargs)
        #Adding CSS classes to the django form
        self.fields['contact_with'].widget.attrs.update({'class':'form-control'})
        self.fields['contact_username'].widget.attrs.update({'class':'form-control'})
        self.fields['contact_avatar'].widget.attrs.update({'class':'form-control'})
        self.fields['contact_email'].widget.attrs.update({'class':'form-control'})
        self.fields['contact_tel'].widget.attrs.update({'class':'form-control'})
        

################## MESSAGE SECTION ###################

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message 
        fields = {"message_from","message_to","message_body"}
        #Hiding id of logged in client
        widgets = {"message_from":forms.HiddenInput(),"message_to":forms.HiddenInput()}
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args,**kwargs)

        #Adding CSS classes to the django form
        self.fields['message_body'].widget.attrs.update({'class':'form-control form-control-lg','id':'exampleFormControlInput1', 'style':'height:20px; margin-top: 10px;' })
       
        
        




