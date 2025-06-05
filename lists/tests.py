import pytest
import re
from django.core.urlresolvers import resolve

from lists.views import home_page
from lists.models import Item, List


# No more TestCase subclassing for test classes

def test_root_url_resolves_to_home_page_view():
    found = resolve('/')
    assert found.func == home_page

@pytest.mark.django_db
def test_home_page_returns_correct_html(client):
    response = client.get('/')
    assert response.templates[0].name == 'home.html'
    # For assertContains, check content directly
    # Example: assert b"A new list item" in response.content

@pytest.mark.django_db
def test_only_saves_items_when_necessary(client):
    client.get('/')
    assert Item.objects.count() == 0


@pytest.mark.django_db
def test_saving_and_retrieving_items():
    list_ = List.objects.create()
    first_item = Item(text='Item 1 da lista', list=list_)
    first_item.save()
    item_id = first_item.id
    item = Item.objects.get(id=item_id)
    assert first_item.text in item.text

@pytest.mark.django_db
def test_list_items():
    List.objects.create() # Create a list for items to belong to
    Item(text='item1', list=List.objects.first()).save()
    List.objects.create() # Create another list
    Item(text='item2', list=List.objects.last()).save() # Assign to the second list
    assert Item.objects.count() == 2


@pytest.mark.django_db
def test_display_only_items_for_that_list(client):
    correct_list = List.objects.create()
    Item.objects.create(text='itemey 1', list=correct_list)
    Item.objects.create(text='itemey 2', list=correct_list)

    other_list = List.objects.create()
    Item.objects.create(text='other itemey 1', list=other_list)
    Item.objects.create(text='other itemey 2', list=other_list)

    response = client.get(f'/lists/{correct_list.id}/')

    assert 'itemey 1' in response.content.decode()
    assert 'itemey 2' in response.content.decode()
    assert 'other itemey 1' not in response.content.decode()
    assert 'other itemey 2' not in response.content.decode()

@pytest.mark.django_db
def test_uses_list_template(client):
    list_ = List.objects.create()
    response = client.get(f'/lists/{list_.id}/')
    assert response.templates[0].name == 'list.html'


@pytest.mark.django_db
def test_can_save_a_POST_request(client):
    client.post('/lists/new', data={'item_text': 'A new list item'})
    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new list item'

@pytest.mark.django_db
def test_redirects_after_POST(client):
    response = client.post('/lists/new', data={'item_text': 'A new list item'})
    new_list = List.objects.first()
    assert response.status_code == 302
    assert response.url == f'/lists/{new_list.id}/'


@pytest.mark.django_db
def test_create_list():
    list_ = List()
    list_.save()
    saved_list = List.objects.first()
    assert saved_list == list_

    first_item = Item(text='The first (ever) list item')
    first_item.list = list_
    first_item.save()

    second_item = Item(text='Item the second')
    second_item.list = list_
    second_item.save()

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    assert Item.objects.filter(list=list_).count() == 2


@pytest.mark.django_db
def test_can_save_a_POST_request_to_an_existing_list(client):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    client.post(
        f'/lists/{correct_list.id}/add_item',
        data={'item_text': 'A new item for an existing list'}
    )

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new item for an existing list'
    assert new_item.list == correct_list

@pytest.mark.django_db
def test_redirect_to_list_view(client):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f'/lists/{correct_list.id}/add_item', # Corrected URL from 'add_items' to 'add_item'
        data={'item_text': 'A new item for an existing list'}
    )

    assert response.status_code == 302
    assert response.url == f'/lists/{correct_list.id}/'
