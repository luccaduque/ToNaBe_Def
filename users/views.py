from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib import messages

def cadastro(request):
    if request.method == "GET":
        return render(request, 'users/cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username).first()

        if user:
            messages.error(request, 'Este username já está em uso!')
            return render(request, 'users/cadastro.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('sistema:pagina_principal')


def login(request):
    if request.method == "GET":
        return render(request, 'users/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            login_django(request, user)
            messages.success(request, f'Bem-vindo de volta, {username}!')
            return redirect('sistema:pagina_principal')
        
        else:
            messages.error(request, 'Username ou senha inválidos!')
            return render(request, 'users/login.html')

#@login_required (login_url='/users/login/')       
 #def sistema(request):
    #if request.user.is_authenticated:
        #return HttpResponse('Autenticado no sistema')

