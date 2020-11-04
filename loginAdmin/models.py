from django.db import models

# Create your models here.
class administrador(models.Model):
    Correo=models.EmailField(max_length=25)
    contraseña=models.CharField(max_length=100)

    def __str__(self):
        return self.Correo