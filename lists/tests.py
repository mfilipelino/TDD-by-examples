from django.test import TestCase
from django.core.urlresolvers import resolve # Changed import for Django 1.8 compatibility

from lists.views import home_page
from lists.models import Item, List


class HomePageViewTest(TestCase): # Renamed ListTestCase to HomePageViewTest
    # Test that the root URL resolves to the home_page view function.
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    # Test that the home page returns the correct HTML template.
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    # Test that items are only saved to the database when necessary (e.g., not on a GET request to home page).
    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelPersistenceTest(TestCase): # Renamed ItemModelTest to ItemModelPersistenceTest
    # Test that a single item can be saved and then retrieved from the database.
    def test_saving_and_retrieving_items(self):
        first_item = Item(text='Item 1 da lista', list=List.objects.create())
        first_item.save()
        item_id = first_item.id
        item = Item.objects.get(id=item_id)
        self.assertIn(first_item.text, item.text)

    # Test that multiple items can be saved and the total count is correct.
    def test_can_save_and_retrieve_multiple_items(self): # Renamed test_list_items to test_can_save_and_retrieve_multiple_items
        Item(text='item1', list=List.objects.create()).save()
        Item(text='item2', list=List.objects.create()).save()
        self.assertEqual(Item.objects.count(), 2)


class ListViewAndItemDisplayTest(TestCase): # Renamed ListViewTest to ListViewAndItemDisplayTest

    # Test that the list view displays only items belonging to that specific list.
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

    # Test that the list view uses the 'list.html' template.
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

    # Test viewing an empty list, ensuring it displays correctly without errors.
    def test_view_empty_list(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertEqual(response.status_code, 200)
        # Assuming a message for empty lists, this might need adjustment based on actual template
        self.assertContains(response, 'Your list is empty.', count=0, status_code=200)


    # Test attempting to view a non-existent list, expecting a 404 error.
    def test_view_non_existent_list_returns_404(self):
        response = self.client.get('/lists/999/') # Assuming 999 is a non-existent list ID
        self.assertEqual(response.status_code, 404)


class NewListCreationTest(TestCase): # Renamed NewListTest to NewListCreationTest
    # Test that a POST request to '/lists/new' can save a new list item.
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    # Test that after a POST request to '/lists/new', the user is redirected to the new list's page.
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))

    # Test that attempting to save an empty item text results in not creating an item.
    # Further validation (e.g., form errors) would be tested in form tests.
    def test_cannot_save_empty_list_item(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(Item.objects.count(), 0)


class ListAndItemRelationshipTest(TestCase): # Renamed ListAndItemModels to ListAndItemRelationshipTest
    # Test creating a list and adding items to it, ensuring the relationship is maintained.
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


class AddItemToExistingListTest(TestCase): # Renamed NewItemTest to AddItemToExistingListTest

    # Test that a POST request to '/lists/<list_id>/add_item' saves an item to the specified existing list.
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post( # Corrected variable name from request to _
            '/lists/{}/add_item'.format(correct_list.id),
            data=dict(item_text='A new item for an existing list')
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    # Test that after adding an item to an existing list, the user is redirected back to that list's view.
    def test_redirect_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/add_item'.format(correct_list.id), # Corrected URL from 'lists/{}/add_items' to '/lists/{}/add_item'
            data=dict(item_text='A new item for an existing list')
        )

        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id)) # Corrected redirect URL

    # Test that attempting to save an empty item to an existing list does not create a new item.
    # Specific error handling or form validation would be part of form tests.
    def test_cannot_save_empty_list_item_to_existing_list(self):
        list_ = List.objects.create()
        self.client.post(
            '/lists/{}/add_item'.format(list_.id),
            data={'item_text': ''}
        )
        self.assertEqual(Item.objects.filter(list=list_).count(), 0)
