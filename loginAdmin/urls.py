from loginAdmin.views import agregarNuevo, out
from django.urls import path
from loginAdmin import views

app_name="mp"
urlpatterns = [
    path("login/",views.login,name="login"),
    #path("registrar/",views.registrar,name="registrar"),
    path("index/",views.index,name="index"),
    path("out/",views.out,name="out"),
    path("modificar/<int:id>",views.modificarMP,name="modificarMP"),
    path("modificar/agregar/",views.agregarNuevo,name="agregar")
]