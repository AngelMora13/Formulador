from django.db.models import fields
from rest_framework import serializers
from loginAdmin.models import administrador

class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model=administrador
        fields=("id","Correo","contraseña")