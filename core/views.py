from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from . import constants as consts, models
from django.contrib import messages
from weasyprint import HTML
import requests
import tempfile

def livros(request):
    params = {
        'q': 'programação',
        'key': consts.KEY,
        'maxResults': 20,
        'langRestrict': 'pt',
    }
    
    if request.method == 'POST':
        categoria = request.POST.get('categoria')
        nome = request.POST.get('nome')
        autor = request.POST.get('autor')
        try:
            qtd = int(request.POST.get('qtd'))
        except:
            qtd = 20
        
        params = {
            'key': 'AIzaSyC-i-x3e_trJqkqbWAWBdbYmadX_RZ5xh4',
            'langRestrict': 'pt',
        }

        print(categoria, nome, autor, qtd)
        
        consulta = []
        if categoria:
            consulta.append(f'subject:{categoria.strip()}')

        if nome:
            consulta.append(f'intitle:{nome.strip()}')
            
        if autor:
            consulta.append(f'inauthor:{autor.strip()}')
        if qtd:
            params['maxResults'] = qtd
        else:
            params['maxResults'] = 20

        params = {
            'q': '+'.join(consulta),
        }

    try:
        response = requests.get(consts.URL, params=params)

        data = response.json()
        livros = data.get('items', [])
    except Exception as e:
        messages.add_message(request, constants.ERROR, 'Erro ao consultar livros: %s' %e)

    qtd_carrinho = models.Carrinho.objects.filter(status='ABERTO').count()
    
    return render(request,
                  'lista-livros.html',
                  { 
                    'livros': livros,
                    'qtd_carrinho': qtd_carrinho
                  })

def detalhar_livro(request, id):
    response = requests.get(f'{consts.URL}/{id}')
    book = response.json()
    data_publicacao = str(book.get('volumeInfo').get('publishedDate'))
    print(data_publicacao)
    if '-' in data_publicacao:
        if len(data_publicacao.split('-')) == 3:
            _y, _m, _d = data_publicacao.split('-')
            data_publicacao = f'{_d}/{_m}/{_y}'
        elif len(data_publicacao.split('-')) == 2:
            _y, _m = data_publicacao.split('-')
            data_publicacao = f'{_m}/{_y}'
        
    categrias = []
    
    if book.get('volumeInfo').get('categories'):
        for c in book.get('volumeInfo').get('categories'):
            if '/' in c:
                for sub in c.split('/'):
                    if sub not in categrias:
                        categrias.append(sub)
            else:
                if sub not in categrias:
                    categrias.append(c)
                    
    qtd_carrinho = models.Carrinho.objects.filter(status='ABERTO').count()
    
    return render(request, 
                  'detalhar-livro.html', 
                  {
                      'book': book,
                      'data_publicacao': data_publicacao,
                      'categorias': categrias,
                      'qtd_carrinho': qtd_carrinho
                  })

def compras(request):
    if request.method == 'POST':
        try:
            for carrinho in models.Carrinho.objects.filter(status='ABERTO'):
                carrinho.status='FECHADO'
                carrinho.save()
            messages.add_message(request, constants.SUCCESS, 'Compra finalizada com sucesso!')
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro ao finalizar compra, erro: %s' %e)
        
    qtd_carrinho = models.Carrinho.objects.filter(status='ABERTO').count()
    compras = models.Carrinho.objects.all().exclude(status='ABERTO')
    
    return render(request, 
                  'compras.html',
                  {
                      'qtd_carrinho': qtd_carrinho,
                      'compras': compras
                  })

def carrinho(request):
    qtd_carrinho = models.Carrinho.objects.filter(status='ABERTO').count()
    items = models.Carrinho.objects.filter(status='ABERTO')
    valor_total = 0.00
    for item in items:
        valor_total = item.valor*item.quantidade
        
    return render(request, 
                  'carrinho.html',
                  {
                      'items': items,
                      'qtd_carrinho': qtd_carrinho,
                      'valor_total': valor_total
                  })

def remover_item(request, id):
    try:
        item = models.Carrinho.objects.get(livro_id=id, status='ABERTO')
        if item.quantidade > 1:
            item.quantidade += 1
            item.save()
            messages.add_message(request, constants.SUCCESS, 'Diminuído quantudade do item!')
        else:
            item.delete()
            messages.add_message(request, constants.SUCCESS, 'Item removido do carrinho!')
    except Exception as e:
        messages.add_message(request, constants.ERROR, 'Erro ao remover item do carrinho, erro: %s' %e)

    return redirect('carrinho')
    
def adicionar_carrinho(request, id):
    response = requests.get(f'{consts.URL}/{id}')
    book = response.json()

    thumbnail = ''
    try:
        if book.get('volumeInfo').get('imageLinks').get('thumbnail'):
            thumbnail = book.get('volumeInfo').get('imageLinks').get('thumbnail')
    except:
        pass
        
    if models.Carrinho.objects.filter(livro_id=book.get('id'), status='ABERTO').count() < 1:
        try:
            models.Carrinho.objects.create(
                livro_id = book.get('id'),
                selfLink = book.get('selfLink'),
                title = book.get('volumeInfo').get('title'),
                thumbnail = thumbnail,
                quantidade = 1,
                valor = 0.00
            )
            messages.add_message(request, constants.SUCCESS, 'Item adicionado ao carrinho!')
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro ao adcionar item ao carrinho, erro: %s' %e)
            
    else:
        try:
            item = models.Carrinho.objects.get(livro_id=book.get('id'), status='ABERTO')
            item.quantidade += 1
            item.save()
            messages.add_message(request, constants.SUCCESS, f'Adicionado quantidade do item {item} ao seu carrinho!')
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro ao adcionar quantidade ao carrinho, erro: %s' %e)
    return redirect('/')


def adicionar_item(request, id):
    try:
        item = models.Carrinho.objects.get(livro_id=id, status='ABERTO')
        item.quantidade += 1
        item.save()
        messages.add_message(request, constants.SUCCESS, f'Adicionado quantidade do item {item} ao seu carrinho!')
    except Exception as e:
        messages.add_message(request, constants.ERROR, 'Erro ao adcionar item ao carrinho, erro: %s' %e)
        
    return redirect('carrinho')


def limpar_carrinho(request):
    try:
        models.Carrinho.objects.filter(status='ABERTO').delete()
        messages.add_message(request, constants.SUCCESS, 'Todos os item do carrinho foram removidos!')
    except Exception as e:
        messages.add_message(request, constants.ERROR, 'Erro ao remover item do carrinho, erro: %s' %e)

    return redirect('livros')

def exportar_pdf(request):
    compras = models.Carrinho.objects.all().exclude(status='ABERTO')
    
    # Renderiza o template HTML
    html_string = render_to_string('relatorio-pdf.html', 
                                   {
                                        'compras': compras
                                    })
    
    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=True, suffix='.pdf') as temp:
        HTML(string=html_string).write_pdf(temp.name)
        temp.seek(0)
        pdf = temp.read()
        
    # Cria a resposta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response