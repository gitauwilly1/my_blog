from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = { 'name': 'John Doe',}
    return render(request, 'index.html', context)

def about(request):
    context = { 'name': 'John Doe',}
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')