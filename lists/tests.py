from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item, List


class ListTestCase(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item(text='Item 1 da lista', list=List.objects.create())
        first_item.save()
        item_id = first_item.id
        item = Item.objects.get(id=item_id)
        self.assertIn(first_item.text, item.text)

    def test_list_items(self):
        Item(text='item1', list=List.objects.create()).save()
        Item(text='item2', list=List.objects.create()).save()
        self.assertEqual(Item.objects.count(), 2)


class ListViewTest(TestCase):

    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other itemey 1', list=other_list)
        Item.objects.create(text='other itemey 2', list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other itemey 1')
        self.assertNotContains(response, 'other itemey 2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))


class ListAndItemModels(TestCase):
    def test_create_list(self):
        list_ = List()
        list_.save()
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        first_item = Item(text='The first (ever) list item')
        first_item.list = list_
        first_item.save()

        second_item = Item(text='Item the second')
        second_item.list = list_
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(Item.objects.filter(list=list_).count(), 2)


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        request = self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data=dict(item_text='A new item for an existing list')
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            'lists/{}/add_items',
            data=dict(item_text='A new item for an existing list')
        )

        self.assertRedirects(response, 'lists/{}/'.format(correct_list.id))
