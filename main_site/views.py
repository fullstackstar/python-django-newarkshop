from django.shortcuts import render


def index(request):
    """The home page for Newark Shop."""
    return render(request, 'main_site/index.html')
