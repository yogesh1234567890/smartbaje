from django.shortcuts import render

# Create your views here.

def viewpage(request):
    return render(request,"viewfront/index-4.html")

def viewpage1(request):
    return render(request,"viewfront/index-4.html")