# Generated by Django 5.0.7 on 2024-08-03 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_carrinho_livro_carrinho_livro_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrinho',
            name='thumbnail',
            field=models.TextField(blank=True, null=True, verbose_name='Thumbnail'),
        ),
    ]
