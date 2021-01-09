# Generated by Django 3.1.2 on 2021-01-09 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MateriasPrimas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=30)),
                ('Humedad', models.IntegerField()),
                ('Proteina', models.IntegerField()),
                ('Grasa', models.IntegerField()),
                ('Fibra', models.IntegerField()),
                ('Cenizas', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='usoFormulador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_created=True, auto_now=True)),
                ('vecesUsado', models.IntegerField()),
                ('obtencionResultado', models.IntegerField()),
            ],
        ),
    ]
