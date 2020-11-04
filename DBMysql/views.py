from django.shortcuts import redirect, render

from django.http.response import JsonResponse
from requests.api import request
from rest_framework.parsers import JSONParser
from rest_framework import status



from DBMysql.models import MateriasPrimas
from DBMysql.DBSerializer import DBSerializer
from rest_framework.decorators import api_view


# Create your views here.

@api_view(["GET","POST","DELETE"])
def listadoMP(request):
    if request.method=="GET":
        materiaPrima=MateriasPrimas.objects.all()

        #si la busqueda es por el nombre, aplico un filtro, sino busco a todos
        Nombre=request.GET.get("Nombre",None)
        if Nombre is not None:
            materiaPrima=materiaPrima.filter(Nombre__icontains=Nombre)
        #fin del filtro
        DB_Serializer=DBSerializer(materiaPrima,many=True)
        return JsonResponse(DB_Serializer.data,safe=False)
        #safe=false para onjetos serializer

    #crea y guarda una nueva materia prima
    elif request.method=="POST":
        nuevaMateriaPrima=JSONParser().parse(request)
        DB_Serializer=DBSerializer(data=nuevaMateriaPrima)
        if DB_Serializer.is_valid():
            DB_Serializer.save()
            return JsonResponse(DB_Serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(DB_Serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=="DELETE":
        if request.session["user"]: 
            contador=MateriasPrimas.objects.all().delete()
            return JsonResponse({"message":"{} las materias primas fueron eliminadas satisfactoriamente".format(contador[0])},status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({'error': 'authentication failed'})

@api_view(["GET","DELETE","POST"])
def modificar(request,id):
        #return JsonResponse({'error': 'authentication failed'})
    #buscar si el elemento id existe
    try:
        materiaPrimaId=MateriasPrimas.objects.get(id=id)
    except MateriasPrimas.DoesNotExist:
        return JsonResponse({"message":"la materia prima no existe"},status=status.HTTP_404_NOT_FOUND)

    #entregar una materia prima por su id
    if request.method=="GET": 
        DB_serializer=DBSerializer(materiaPrimaId)
        return JsonResponse(DB_serializer.data)
    #actualizar una materia prima pro su id
    elif request.method=="POST":
        materiaPrima_datos=JSONParser().parse(request)
        DB_serializer=DBSerializer(materiaPrimaId,data=materiaPrima_datos)
        if DB_serializer.is_valid():
            DB_serializer.save()
            return JsonResponse(DB_serializer.data)

        return JsonResponse(DB_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    #ELIMINAR UNA MATERIA PRIMA
    elif request.method=="DELETE":
        materiaPrimaId.delete()
        return JsonResponse({'message':'la materia prima fue eliminada de forma satisfactoria'},status=status.HTTP_204_NO_CONTENT)
        
    return redirect("/api/noautorizado") 

def error(request):
    return render(request,"sinPermiso.html") 
