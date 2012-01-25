from mainpage.models import  Seller, Product, Category
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def main_index(request):

    msg = "Showcase!!!"
    return render_to_response('main/index.html',{
    'message':msg,},
    context_instance = RequestContext(request))

