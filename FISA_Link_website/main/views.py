from django.shortcuts import render # type: ignore
from django.shortcuts import redirect # type: ignore

def index(request):
    return render(request, 'index.html')

def sign_up(request):
    return render(request, 'sign_up.html')

def mail_valide(request):
    return render(request, 'mail_valide.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def sif(request):
    return render(request, 'sif.html')

def redirect_index(request):
    return redirect('/')
