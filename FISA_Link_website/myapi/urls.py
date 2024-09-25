from django.urls import path # type: ignore
from .views import *

urlpatterns = [
    #path('api/users/', get_users, name='get_users'),
    path('api/login/', login_user, name='login_user'),
    path('api/sign_up/', register_user, name='register_user'),
    path('api/verify-email/', validate_mail, name='validate_mail'),
    path('api/dashboard/', dashboard, name='dashboard'),
    path('api/logout/', logout_user, name='logout'),
    path('api/auto_login/', auto_login, name='auto_login'),
    path('api/get_sif_status/', get_sif_status, name='get_sif_status'),
    path('api/set_sif_status/', set_sif_status, name='set_sif_status'),
    path('api/set_sif_change_bungalow/', set_sif_change_bungalow, name='set_sif_change_bungalow'),
    path('api/set_sif_change_pizza/', set_sif_change_pizza, name='set_sif_change_pizza'),
    path('api/get_paiement_sif/', get_paiement_sif, name='get_paiement_sif'),
]
