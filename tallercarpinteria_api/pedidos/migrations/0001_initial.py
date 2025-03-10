# Generated by Django 5.1.6 on 2025-03-05 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente_nombre', models.CharField(max_length=255)),
                ('estado', models.CharField(max_length=50)),
                ('fecha_medicion', models.DateField()),
                ('presupuesto', models.FloatField()),
                ('fecha_llegada_materiales', models.DateField()),
                ('fecha_entrega', models.DateField()),
                ('ruta_plano', models.CharField(max_length=255)),
                ('notas', models.TextField()),
            ],
        ),
    ]
