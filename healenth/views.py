from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def procedimentos(request):
    return render(request, "procedimentos.html")


def faq(request):
    return render(request, "faq.html")


def quemsomos(request):
    return render(request, "quemsomos.html")


def termos(request):
    return render(request, "termos.html")


def agendamedica(request):
    return render(request, "agendamedica.html")


def gestao(request):
    return render(request, "gestao.html")


def prontuario(request):
    return render(request, "prontuario.html")


def sugestoes(request):
    return render(request, "sugestoes.html")
