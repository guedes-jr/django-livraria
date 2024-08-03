from django.db import models

class Carrinho(models.Model):
    livro_id = models.CharField(max_length=50, null=True, blank=True)
    selfLink = models.CharField(max_length=200, verbose_name="link", null=True, blank=True)
    title = models.CharField(max_length=50, verbose_name="Titulo", null=True, blank=True)
    thumbnail = models.TextField(verbose_name="Thumbnail", null=True, blank=True)
    quantidade = models.IntegerField(default=0)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor do item")
    status = models.TextField(verbose_name="status", default='ABERTO')
    
    def __str__(self):
        return f'{self.title}'