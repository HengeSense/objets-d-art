from project.models import Objet, Client, Customer, Cart, Coupon
from project.backend.googlecheckout import Cart
from django.shortcuts import render_to_response

def index(request):
    # get 2 sales
    # get 5 news items
    # display render these two 

def news(request, page = 1):

def sales(request):

def simple_search(request):

def power_search(request):

def calendar(request):

def get_objet_by_id(request, id):

def get_objet_by_slug(request, slug):

def get_creator(request, user_name):

def list_by_tag(request):

def list_by_composer(request):

def handle_cart(request, cart_name = 'default'):

def create_user(request):

def handle_feedback(request):

def _add_item(cart, item):

def _del_item(cart, index):

def _add_cart(cart_name):

def _del_cart(cart):
