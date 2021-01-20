from django.db import models

# Create your models here.

class MateriasPrimas(models.Model):
    Nombre=models.CharField(max_length=30)
    Humedad=models.FloatField()
    Proteina=models.FloatField()
    Grasa=models.FloatField()
    Fibra=models.FloatField()
    Cenizas=models.FloatField()
    
    def __str__(self):
        return self.Nombre
class usoFormulador(models.Model):
    vecesUsado=models.IntegerField()
    obtencionResultado=models.IntegerField()
    fecha=models.DateField(auto_created=True,auto_now=True)
    def __str__(self):
        return self.vecesUsado