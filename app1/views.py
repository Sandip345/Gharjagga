from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import FormView
from . import forms
from . import models
import logging
from django.contrib.auth import login,authenticate
from django.contrib import messages
# Create your views here.

class homeview(ListView):
    template_name='home_list.html'
    paginate_by = 9
    queryset=models.Product.objects.active().order_by('-date_updated')
    context_object_name='products'

class contactus(FormView):
    template_name="contact_us.html"
    form_class=forms.ContactForm
    success_url="/"

    def form_valid(self,form):
        form.send_mail()
        response = super().form_valid(form)
        messages.info(
        self.request,"Thank you for contacting us. We will response to you soon."
        )
        return response
        
        
class sellproducts(FormView):
    template_name="sell_products.html"
    form_class=forms.SellProductsForm
    success_url="/"
    
    def form_valid(self,form):
      response = super().form_valid(form)
      form.save()
      messages.info(
        self.request,"Your form has been submitted. We will verify and post it as soon as possible."
        )
      return response

class ProductListView(ListView):
    template_name="app1/home_list.html"
    paginate_by = 4

    def get_queryset(self,*args,**kwargs):
        tag = self.kwargs['name']
        self.tag = None
        if tag != "allproducts":
            self.tag=get_object_or_404(
            models.ProductTag,slug=tag
            )
        if self.tag:
            products=models.Product.objects.active().filter(
            tags=self.tag
            )
        else:
            products=models.Product.objects.active()

        return products.order_by("name")

logger=logging.getLogger(__name__)
class SignupView(FormView):
    template_name="signup.html"
    form_class=forms.UserCreationForm

    def get_success_url(self):
        redirect_to=self.request.GET.get("next","/")
        return redirect_to

    def form_valid(self,form):
        response=super().form_valid(form)
        form.save()
        email=form.cleaned_data.get("email")
        raw_password=form.cleaned_data.get("password1")
        logger.info(
        "New signup for email=%s through SignupView",email
        )
        user=authenticate(email=email,password=raw_password)
        login(self.request,user)
        form.send_mail()
        messages.info(
        self.request,"You signed up successfully."
        )
        return response
       
class savedproducts(TemplateView):
  template_name='saved_items.html'
