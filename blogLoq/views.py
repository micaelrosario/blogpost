from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Esta é uma rota de teste no Django.")
