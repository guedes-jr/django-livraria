from django.urls import path
from . import views

urlpatterns = [
    path('', views.livros, name="livros"),
    path('detalhar/<str:id>', views.detalhar_livro, name="detalhar_livro"),
    path('carrinho', views.carrinho, name="carrinho"),
    path('carrinho/adicionar/<str:id>', views.adicionar_carrinho, name="adicionar_carrinho"),
    path('carrinho/item/<str:id>', views.adicionar_item, name="adicionar_item"),
    path('carrinho/remover/<str:id>', views.remover_item, name="remover_item"),
    path('carrinho/limpar/', views.limpar_carrinho, name="limpar_carrinho"),
    path('compras/', views.compras, name="compras"),
    path('compras/exportar/', views.exportar_pdf, name="exportar_pdf"),
]
