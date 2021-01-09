from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import exceptions, status

from DBMysql.models import MateriasPrimas
from DBMysql.DBSerializer import DBSerializer
from rest_framework.decorators import api_view

from cvxopt.modeling import op,variable


# Create your views here.

@api_view(["GET"])
def listadoMP(request):
    if request.method=="GET":
        materiaPrima=MateriasPrimas.objects.all().order_by("Nombre")
        #si la busqueda es por el nombre, aplico un filtro, sino busco a todos
        Nombre=request.GET.get("Nombre",None)
        if Nombre is not None:
            materiaPrima=materiaPrima.filter(Nombre__icontains=Nombre)
        #fin del filtro
        DB_Serializer=DBSerializer(materiaPrima,many=True)
        return JsonResponse(DB_Serializer.data,safe=False)
        #safe=false para onjetos serializer

@api_view(["POST"])
def formular(request):
    if request.method=="POS":
        valores=JSONParser().parse(request)
        try:
            minimo=valores[0][0]
            maximo=valores[0][1]
            ingredientesId=valores[1]
        except TypeError:
            raise exceptions.APIException("Error al enviar datos")
        obj=m1=m2=p1=p2=h1=h2=g1=g2=0
        c=[]
        try:
            for x in ingredientesId:
                x["id"]=MateriasPrimas.objects.get(id=x["id"])
                x["Nombre"]=variable()
                c1=(x["Nombre"]>=0)
                c.append(c1)
                m1+=x["Nombre"]
                p1+=x["id"].Proteina*x["Nombre"]
                h1+=x["id"].Humedad*x["Nombre"]
                g1+=x["id"].Grasa*x["Nombre"]

                obj+=x["Nombre"]

            m2=(m1<=maximo["Masa"])
            p2=(p1/minimo["Masa"]<=maximo["Proteina"])
            h2=(h1/minimo["Masa"]<=maximo["Humedad"])
            g2=(g1/minimo["Masa"]<=maximo["Grasa"])

            m1=(m1>=minimo["Masa"])
            p1=(p1/minimo["Masa"]>=minimo["Proteina"])
            h1=(h1/minimo["Masa"]>=minimo["Humedad"])
            g1=(g1/minimo["Masa"]>=minimo["Grasa"])

            c.extend([m1,m2,p1,p2,h1,h2,g1,g2])

            fx=op(obj,c)
            fx.solve(verbose=False,options={'show_progress': False})
        except ZeroDivisionError:
            raise exceptions.APIException("La Masa esperada no puede ser cero (0)")
        except TypeError:
            raise exceptions.APIException("Valor ingresado no numerico")
        except MateriasPrimas.DoesNotExist:
            raise exceptions.APIException("El ingrediente no esta en la base de datos, Contactenos")

        mp=[]
        try:
            for x in ingredientesId:
                x["Masa"]=x["Nombre"].value[0]
                mp.append(x["Masa"])
            return JsonResponse(mp,safe=False,status=status.HTTP_200_OK)
        except TypeError:
            raise exceptions.APIException("Los datos suministrados no llevan aun resultado optimo")
    else:
        return JsonResponse("Metodo no permitido", status=status.HTTP_400_BAD_REQUEST)

