from django.shortcuts import render, redirect
from .forms import ContatoForm, SugestoesForm


def contato_view(request):
    if request.method == "POST":
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("contato:contact-us")
    else:
        form = ContatoForm()

    return render(request, "contato/faleconosco.html", {"form": form})


def sugestao_view(request):
    if request.method == "POST":
        form = SugestoesForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("contato:review-us")
    else:
        form = SugestoesForm()
    return render(request, "contato/sugestoes.html", {"form": form})
