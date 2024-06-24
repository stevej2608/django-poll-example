from django.shortcuts import render


def router(request, pk=None):
    return render(request, "index.html", {})
