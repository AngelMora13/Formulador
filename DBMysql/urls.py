from django.urls import path
from DBMysql import views
app_name="api"
urlpatterns = [
    path("materiaprima/",views.listadoMP,name="listadoMP"),
    path("materiaprima/<str:id>",views.modificar,name="modificar"),
    path("noautorizado/",views.error,name="noauth")
]
