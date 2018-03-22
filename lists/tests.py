from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item


class ListTestCase(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertIn('A new list item', response.context.get('new_item_text'))
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)



class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'Item 1 da lista'
        first_item.save()
        item_id = first_item.id
        item = Item.objects.get(id=item_id)
        self.assertIn(first_item.text, item.text)

    def test_list_items(self):
        Item(text='item1').save()
        Item(text='item2').save()
        self.assertEqual(Item.objects.count(), 2)
