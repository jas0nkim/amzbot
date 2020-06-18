from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'frontend/index.html')

@login_required
def pricewatching(request):
    return render(request, 'frontend/pricewatching.html', {'title': 'Price Watching List'})
