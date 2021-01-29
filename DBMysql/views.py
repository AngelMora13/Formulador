from django.conf import settings
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from DBMysql.models import MateriasPrimas, usoFormulador
from DBMysql.DBSerializer import DBSerializer, usoFormuladorSerializer
from rest_framework.decorators import api_view

from django.core.mail import EmailMessage

import requests

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
def solveCaptcha(request):    
    if request.method=="POST":  
        contenido=JSONParser().parse(request)   
        try:
            data={
                'response': contenido["recaptcha"],
                'secret': settings.RECAPTCHA_SECRET_KEY
            }
        except KeyError:
            return JsonResponse({"mensaje":"No hay captcha, why you try hack me?"})
        except TypeError:
            return JsonResponse({"mensaje":"No hay captcha, why you try hack me?"})

        resp=requests.post("https://www.google.com/recaptcha/api/siteverify",data=data)
        result_json=resp.json()
        if result_json["success"]==False:
            return JsonResponse({"mensaje":"Como sospechaba, eres un Robot"})
        return JsonResponse({},status=status.HTTP_200_OK)  
    else:
        return JsonResponse({"mensaje":"metodo no permitido"},status=status.HTTP_200_OK)      


@api_view(["POST"])
def enviarCorreo(request):
    if request.method=="POST":      
        contenido=JSONParser().parse(request)   
        try:
            data={
                'response': contenido["recaptcha"],
                'secret': settings.RECAPTCHA_SECRET_KEY
            }
        except KeyError:
            return JsonResponse({"mensaje":"No hay captcha, why you try hack me?"})
        except TypeError:
            return JsonResponse({"mensaje":"No hay captcha, why you try hack me?"})

        resp=requests.post("https://www.google.com/recaptcha/api/siteverify",data=data)
        result_json=resp.json()
        if result_json["success"]==False:
            return JsonResponse({"mensaje":"Como sospechaba, eres un Robot"})
        try:
            email=contenido["correo"]
            contenido["recaptcha"]=result_json
        except KeyError or TypeError:
            return JsonResponse({"mensaje":"No se adjunto el Correo"})
        if email:
            try:
                enviar_correo=requests.post("https://api.mailgun.net/v3/"+settings.EMAIL_BASE_URL+"messages",
                auth = ( "api",settings.EMAIL_API_KEY),
                data = { "from" :email,
                    "to" : [settings.EMAIL_BASE_URL,settings.EMAIL_DEFAULT_SEND],
                    "subject":contenido["asunto"],
                    "text":str(contenido)})
                return JsonResponse({},status=status.HTTP_200_OK)
            except TypeError:
                return JsonResponse({"mensaje":"No se pudo enviar el mensaje"})
            except ConnectionRefusedError:
                return JsonResponse({"mensaje":"No se pudo enviar el mensaje"})            
        else:
            return JsonResponse({"mensaje":"error en los datos"})

@api_view(["POST"])
def formular(request):
    if request.method=="POST":        
        valores=JSONParser().parse(request)
        uso=usoFormulador.objects.all().first()
        if uso is None:
            usoNow={
            "vecesUsado":1,
            "obtencionResultado":0
        }
        else:
            usoNow={
                "vecesUsado":uso.vecesUsado+1,
                "obtencionResultado":uso.obtencionResultado
            }
        try:
            minimo=valores[0][0]
            maximo=valores[0][1]
            ingredientesId=valores[1]
        except TypeError or KeyError:
            return JsonResponse({"mensaje":"error al enviar los datos"})
        obj=m1=m2=p1=p2=h1=h2=g1=g2=f1=f2=cenz1=cenz2=0
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
                f1+=x["id"].Fibra*x["Nombre"]
                cenz1+=x["id"].Cenizas*x["Nombre"]

                obj+=x["Nombre"]

            m2=(m1<=maximo["Masa"])
            p2=(p1/minimo["Masa"]<=maximo["Proteina"])
            h2=(h1/minimo["Masa"]<=maximo["Humedad"])
            g2=(g1/minimo["Masa"]<=maximo["Grasa"])
            f2=(f1/minimo["Masa"]<=maximo["Fibra"])
            cenz2=(cenz1/minimo["Masa"]<=maximo["Cenizas"])


            m1=(m1>=minimo["Masa"])
            p1=(p1/minimo["Masa"]>=minimo["Proteina"])
            h1=(h1/minimo["Masa"]>=minimo["Humedad"])
            g1=(g1/minimo["Masa"]>=minimo["Grasa"])
            f1=(f1/minimo["Masa"]>=minimo["Fibra"])
            cenz1=(cenz1/minimo["Masa"]>=minimo["Cenizas"])

            c.extend([m1,m2,p1,p2,h1,h2,g1,g2,f1,f2,cenz1,cenz2])

            fx=op(obj,c)
            fx.solve(verbose=False,options={'show_progress': False})
        except ZeroDivisionError:
            return JsonResponse({"mensaje":"La Masa esperada no puede ser cero (0)"})
        except TypeError:
            return JsonResponse({"mensaje":"Valor ingresado no numerico"})
        except MateriasPrimas.DoesNotExist:
            return JsonResponse({"mensaje":"El ingrediente no esta en la base de datos, Contactenos"})

        mp=[]
        try:
            for x in ingredientesId:
                x["Masa"]=x["Nombre"].value[0]
                mp.append(x["Masa"])
            if uso is None:
                usoNow["obtencionResultado"]=1
            else:
                usoNow["obtencionResultado"]=uso.obtencionResultado+1
            uso_Serializer=usoFormuladorSerializer(uso,data=usoNow)
            if uso_Serializer.is_valid():
                uso_Serializer.save()
            return JsonResponse(mp,safe=False,status=status.HTTP_200_OK)
        except TypeError:
            uso_Serializer=usoFormuladorSerializer(uso,data=usoNow)
            if uso_Serializer.is_valid():
                uso_Serializer.save()            
            return JsonResponse({"mensaje":"Los datos suministrados no llevan a un resultado optimo"})
    else:
        return JsonResponse({"mensaje":"Metodo no permitido"})
