from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Esta é uma rota de teste no Django.")

def index_view(request):
    return HttpResponse("Bem-vindo à página inicial do blog!") 