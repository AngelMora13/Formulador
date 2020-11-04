from copy import error
from django.urls import path
from DBMysql import views

urlpatterns = [
    path("materiaprima/",views.listadoMP,name="listadoMP"),
    path("materiaprima/<str:id>",views.modificar,name="modificar"),
    path("noautorizado/",views.error,name="noauth")
]
