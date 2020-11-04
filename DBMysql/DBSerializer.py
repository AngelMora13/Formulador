from rest_framework import serializers
from DBMysql.models import MateriasPrimas

class DBSerializer(serializers.ModelSerializer):
    class Meta:
        model=MateriasPrimas
        fields=("id","Nombre","Humedad","Proteina","Grasa")
        
