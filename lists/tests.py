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
        self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), '/lists/the-only-list-in-the-world/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_display_all_list_items(self):
        #prepare
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        #execute
        response = self.client.get('/')

        #assert
        self.assertIn('item 1', response.content.decode())
        self.assertIn('item 2', response.content.decode())


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


class ListViewTest(TestCase):

    def test_display_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')