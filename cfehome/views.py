from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def indexPage(request):
#     print(request.GET['test'])
    return HttpResponse("<b>Hello Django<b>")

def resultPage(request):
    return HttpResponse("<b>Hello Django<b>")

