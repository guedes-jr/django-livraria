# Generated by Django 5.0.7 on 2024-08-03 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_carrinho_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrinho',
            name='status',
            field=models.TextField(default='ABERTO', verbose_name='status'),
        ),
    ]