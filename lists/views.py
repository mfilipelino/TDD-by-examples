from django.shortcuts import render
from lists.models import Item


def home_page(request):

    if request.method == 'POST':
        item = Item.objects.create(text=request.POST.get('item_text', ''))
        new_item_text = item.text
    else:
        new_item_text = ''

    return render(request, 'home.html', dict(new_item_text=new_item_text))
