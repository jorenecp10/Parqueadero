# Generated by Django 4.2.3 on 2023-07-30 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueadero', '0005_remove_parqueadero_cupo_disponible_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parqueadero',
            name='cupo_disponible',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parqueadero',
            name='direccion',
            field=models.CharField(default='default', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='parqueadero',
            name='cupo_maximo',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='parqueadero',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]
