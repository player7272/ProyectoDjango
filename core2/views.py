from django.shortcuts import render

def index(request):
    return render(request, 'core2/index.html')

def home_core2(request):
    return render(request, 'core2/index.html')
