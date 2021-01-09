from django.urls import path
from DBMysql import views
app_name="api"
urlpatterns = [
    path("materiaprima/",views.listadoMP,name="listadoMP"),
    path("formular/",views.formular,name="formular")
    
]
