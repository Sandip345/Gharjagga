from django.urls import path
from . import views
from app1.views import homeview,contactus,ProductListView,SignupView,savedproducts,sellproducts
from django.views.generic import TemplateView,DetailView
from django.conf.urls.static import static
from django.conf import settings
from . import models
from django.contrib.auth import views as auth_views
from app1 import forms

app_name="app1"

urlpatterns=[
path('',homeview.as_view(),name='home'),
path('login/',auth_views.LoginView.as_view(template_name="login.html",form_class=forms.AuthenticationForm,),name="login",),
path('contactus',contactus.as_view(),name='contactus'),
path('signup/',views.SignupView.as_view(),name="signup"),
path('saveditems/',savedproducts.as_view(),name='savedproducts'),
path('sellproducts/',sellproducts.as_view(),name='sellproducts'),
path('products/<slug:name>/',views.ProductListView.as_view(),name="productlist"),
path('product/<slug:slug>/',DetailView.as_view(model=models.Product),name="productdetail")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
