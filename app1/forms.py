from django import forms
from django.forms import ModelForm
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import authenticate
from . import models
import logging
logger=logging.getLogger(__name__)

class ContactForm(forms.Form):
    name=forms.CharField(label='Your name',max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(label='Your email',max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    message=forms.CharField(max_length=600, widget=forms.Textarea(attrs={'class':'form-control','rows': 6}))

    def send_mail(self):
        logger.info("Sending mail to customer service")
        message="From: {0}\nSender Email: {1}\nMessage: {2}".format(
        self.cleaned_data["name"],
        self.cleaned_data["email"],
        self.cleaned_data["message"],
        )
        send_mail(
        "site message",
        message,
        "site@gharjagga.domain",
        ["customerservice@gharjagga.domain"],
        fail_silently=False,
        )
        
        
class SellProductsForm(ModelForm):
    class Meta:
        model=models.Product
        fields=['name','price','location','tags','description','available','active']
        
        widgets={
        'name':forms.TextInput(attrs={'class':'form-control'}),
        'description':forms.Textarea(attrs={'class':'form-control','rows':6}),
        'price':forms.TextInput(attrs={'class':'form-control'}),
        'location':forms.TextInput(attrs={'class':'form-control'})
        }
        

class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model=models.User
        fields=("email",)
        fields_classes={"email":UsernameField}

    def send_mail(self):
        logger.info(
        "sending signup email for email=%s",
        self.cleaned_data["email"],
        )
        message="Welcome{}".format(self.cleaned_data["email"])
        send_mail(
        "Welcome to BookTime",
        message,
        "site@gharjagga.domain",
        [self.cleaned_data["email"]],
        fail_silently=True,
        )

class AuthenticationForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(
    strip=False,widget=forms.PasswordInput
    )

    def __init__(self,request=None,*args,**kwargs):
        self.request=request
        self.user=None
        super().__init__(*args,**kwargs)

    def clean(self):
        email=self.cleaned_data.get("email")
        password=self.cleaned_data.get("password")

        if email is not None and password:
            self.user=authenticate(
            self.request,email=email, password=password
            )
            if self.user is None:
                raise forms.ValidationError(
                "Invalid email/password combination."
                )
            logger.info("Authentication successful for email=%s",email)

        return self.cleaned_data

    def get_user(self):
        return self.user
