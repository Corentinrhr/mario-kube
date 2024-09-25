from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inscription', views.sign_up, name='sign_up'),
    path('mail_valide', views.mail_valide, name='mail_valide'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('sif', views.sif, name='sif'),
    path('lydia_link', views.redirect_index, name='lydia_link'),
    path('paypal_link', views.redirect_index, name='paypal_link'),
]
