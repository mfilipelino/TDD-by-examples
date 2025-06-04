from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound # Import HttpResponseNotFound
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
    except List.DoesNotExist:
        return HttpResponseNotFound('<h1>List not found</h1>') # Return 404 if list does not exist
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items, 'list': list_}) # Pass list to template


def new_list(request):
    list_ = List.objects.create()
    item_text = request.POST.get('item_text', '')
    if item_text: # Only create item if text is not empty
        Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/{}/'.format(list_.id))


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    item_text = request.POST.get('item_text', '')
    if item_text: # Only create item if text is not empty
        Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/{}/'.format(list_.id)) # Corrected redirect URL