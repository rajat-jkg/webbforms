from django.shortcuts import render

# Create your views here.

def docsHome(request):
    return render(request , 'docshome.html' , {'docsactive':'active' })