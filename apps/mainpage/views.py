from apps.mainpage.models import  Seller, Product, Category
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def main(request):
    products = Product.objects.all()
    return render_to_response('main_page.html',{
    	'products':products,},
	    context_instance = RequestContext(request))

def seller(request, slug):
    seller = get_object_or_404(Seller, slug=slug)
    return render_to_response('main/index.html', {
    	'seller':seller
	    }, context_instance=RequestContext(request))

def category(request, slug):
	products = Product.objects.filter(subcategory__slug=slug)
	return render_to_response('category.html', {
		'products': products, },
		context_instance=RequestContext(request))
