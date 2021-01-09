from django.db.models import fields
from rest_framework import serializers
from DBMysql.models import MateriasPrimas, usoFormulador

class DBSerializer(serializers.ModelSerializer):
    class Meta:
        model=MateriasPrimas
        fields=("id","Nombre","Humedad","Proteina","Grasa","Fibra","Cenizas")
        
class usoFormuladorSerializer(serializers.ModelSerializer):
    class Meta:
        model=usoFormulador
        fields=("vecesUsado","obtencionResultado")