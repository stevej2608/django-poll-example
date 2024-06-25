from django.shortcuts import render


def spa_router(request, pk=None, path=None):
    return render(request, "index.html", {})
