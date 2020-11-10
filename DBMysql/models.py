from django.db import models

# Create your models here.

class MateriasPrimas(models.Model):
    Nombre=models.CharField(max_length=30)
    Humedad=models.IntegerField()
    Proteina=models.IntegerField()
    Grasa=models.IntegerField()

    def __str__(self):
        return self.Nombre
    