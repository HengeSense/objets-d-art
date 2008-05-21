from project.models import *
from project.backend.googlecheckout import Cart
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404

def index(request):
    # get 2 sales
    # get 5 news items
    # display render these two 

def news(request, page = 1):

def sales(request):

def simple_search(request):
    if request.GET['q']:
        # search
        q = request.GET['q']
        tag_results = Tag.objects.filter(tag__icontains = q) #XXX find a way to search only internal==false tags
        tag_results += Tag.objects.filter(description__icontains = q)
        score_results = Score.objects.filter(title__icontains = q)
        client_results = Client.objects.filter(full_name__icontains = q)
        return render_to_response('customer/simplesearch_results.html', {'tags': tag_results, 'scores': score_results, 'clients': client_results})
    else:
        # print search form
        return render_to_response('customer/simplesearch.html')

def power_search(request):
    if request.GET['search']:
        # search
        scores = Score.objects.all()
        if request.POST['score_title']:
            scores = scores.objects.filter(title__icontains = request.POST['score_title'])
        if request.POST['composer']:
            scores = scores.objects.filter(client__full_name__icontains = request.POST['composer'])
        if request.POST['difficulty']:
            scores = scores.objects.filter(tag__tag__exact = request.POST['difficulty'])
        if request.POST['ensemble']:
            scores = scores.objects.filter(tag__tag__exact = request.POST['ensemble'])
        if request.POST['category']:
            scores = scores.objects.filter(tag__tag__exact = request.POST['category'])
        if request.POST['max_duration']:
            scores = scores.objects.filter(duration__lte = float(request.POST['max_duration']))
    else:
        # print search form
        return render_to_response('customer/powersearch.html')

def get_objet_by_slug(request, slug):
    score = get_object_or_404(Score, pk = slug)
    return render_to_response('customer/score.html', {'score': score})

def get_creator(request, user_name):
    creator = get_object_or_404(User, pk = user_name)
    if (creator.has_perm('is_client')):
        client = creator.client_set.all()[0] # each User should have only one Client associated with it
        return render_to_response('customer/composer.html', {'client': client})
    else:
        raise Http404

def client_contact(request, user_name):
    creator = get_object_or_404(User, pk = user_name)
    if (creator.has_perm('is_client')):
        client = creator.client_set.all()[0]
        return render_to_response('customer/composer_contact.html', {'client': client})
    else:
        raise Http404

def list_by_tag(request, tag):
    tag_obj = get_object_or_404(Tag, pk = tag)
    scores = tag_obj.scores_set.all()
    return render_to_response('customer/list_by_tag.html', {'scores': scores})

def list_by_composer(request, user_name):
    creator = get_object_or_404(User, pk = user_name)
    if (creator.has_perm('is_client')):
        client = creator.client_set.all()[0]
        scores = client.works.all()
        return render_to_response('customer/list_by_composer', {'client': client, 'scores': scores})
    else:
        raise Http404

def handle_cart(request, cart_name = 'default'):

def create_user(request):

def handle_feedback(request):

def _add_item(cart, item):

def _del_item(cart, index):

def _add_cart(cart_name):

def _del_cart(cart):
