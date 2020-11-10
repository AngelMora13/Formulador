from django.shortcuts import redirect, render
from django.contrib.auth import logout,authenticate,login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from django.http.response import JsonResponse
import requests


from rest_framework.parsers import JSONParser
from rest_framework import status,request

from loginAdmin.models import administrador
from loginAdmin.loginSerializer import loginSerializer

# Create your views here.
def out(request):
    #deslogea
    logout(request)
    return redirect("/loginToAdd/login")


def index(request):
    if request.user.is_authenticated: 
        materiasPrimas=requests.get("http://localhost:8000/api/materiaprima")
        materiasPrimas = materiasPrimas.json()
        usuario=request.user
        return render(request,"index.html",{"usuario":usuario,"materiasprimas":materiasPrimas})

    return redirect("/loginToAdd/login")

def login(request):
    if request.user.is_authenticated: 
        return redirect("/loginToAdd/index",{"user":request.user})
    form=AuthenticationForm()
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
    
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user=authenticate(username=username,password=password)
            if user is not None:
                do_login(request,user)
                return redirect("/loginToAdd/index")
    return render(request,"login.html",{"form":form})

"""
def registrar(request):
    form=formLogin()
    if request.method=="POST":
            form=formLogin(request.POST)

            if form.is_valid():
                nuevouser={
                    "Correo":form.cleaned_data["Correo"],
                    "contraseña":form.cleaned_data["contraseña"]
                }
                nuevoDBUser=loginSerializer(data=nuevouser)
                if nuevoDBUser.is_valid():
                    nuevoDBUser.save()
                    return redirect("/loginToAdd/login")
    messages.error(request,"ha ocurrido un error al agregar el usuario,")
    return render(request,"registrar.html",{'form':form})


class formLogin(forms.Form):
    Correo=forms.EmailField(label="Correo")
    contraseña=forms.CharField(
        label="contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )
"""
def modificarMP(request,id):
    print(request.user.is_authenticated)
    if request.user.is_authenticated: 
        materiasPrimas=requests.get(f"http://localhost:8000/api/materiaprima/{id}")
        mp = materiasPrimas.json()
        form=formModify(initial={
            "Nombre":mp["Nombre"],
            "Humedad":mp["Humedad"],
            "Proteina":mp["Proteina"],
            "Grasa":mp["Grasa"]
            })
        if request.method=="POST":
            form=formModify(request.POST)
            if form.is_valid():
                nombre=form.cleaned_data
                contraseña=form.cleaned_data["Contraseña"]
                requests.post(f"http://localhost:8000/api/materiaprima/{id}",json=nombre,auth=(request.user,contraseña))
                return redirect("/loginToAdd/index")

        return render(request,"modificar.html",{"form":form,"id":id})
    return redirect("/loginToAdd/login")

def agregarNuevo(request):
    if request.user.is_authenticated: 
        form=formModify()
        if request.method=="POST":
            form=formModify(request.POST)
            if form.is_valid():
                nombre=form.cleaned_data
                contraseña=form.cleaned_data["Contraseña"]
                requests.post("http://localhost:8000/api/materiaprima/",json=nombre,auth=(request.user,contraseña))
                return redirect("/loginToAdd/index")
        return render(request,"agregar.html",{"form":form})
    return redirect("/loginToAdd/login")

class formModify(forms.Form):
    Nombre=forms.CharField(label="Nombre")
    Humedad=forms.FloatField(label="Humedad")
    Proteina=forms.FloatField(label="Proteina")
    Grasa=forms.FloatField(label="Grasa")
    Contraseña=forms.CharField(
        label="contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )

