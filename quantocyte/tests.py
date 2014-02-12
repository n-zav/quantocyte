from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from unittest_data_provider import data_provider
from .models import Item


class AuthTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'test@gmail.com', 'test')

    guests_links = lambda: (
        ('Home', reverse('home'), True),
        ('Login', reverse('login'), True),
        ('Logout', reverse('logout'), False),
        ('Items Grid', reverse('grid'), False),
    )

    @data_provider(guests_links)
    def test_guest_links_are_present(self, link_title, link, link_present):
        response = self.client.get('/')
        if link_present:
            self.assertIn(link_title, response.content)
            self.assertIn(link, response.content)
        else:
            self.assertNotIn(link, response.content)

    account_pages = lambda: (
        ('/accounts',),
        ('/accounts/profile',),
    )

    @data_provider(account_pages)
    def test_redirect_account_pages(self, page):
        self.client.login(username='test', password='test')
        response = self.client.get(page, follow="True")
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>Home page</title>', response.content)

    def test_redirect_logout_pages(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('home'))

        self.assertIn('Logout', response.content)

        self.client.logout()
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'), status_code=302)

    user_links = lambda: (
        ('Home', reverse('home'), True),
        ('Logout', reverse('logout'), True),
        ('Login', reverse('login'), False),
        ('Items Grid', reverse('grid'), True),
    )

    @data_provider(user_links)
    def test_user_links_are_present(self, link_title, link, link_present):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        if link_present:
            self.assertIn(link_title, response.content)
            self.assertIn(link, response.content)
        else:
            self.assertNotIn(link, response.content)


class GridTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Jane', 'jane.doe@gmail.com',
                                             'test')
        self.client.login(username='Jane', password='test')
        self.item = Item.objects.create(name='Anastasiia', id='1')

    def test_items_grid_page(self):
        response = self.client.get(reverse('grid'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('$("#item-grid")', response.content)
        self.assertIn("Logout", response.content)

    def test_added_item_in_grid(self):
        name = 'Vasya'
        count = Item.objects.filter(name=name).count()
        self.assertEqual(0, count)

        self.client.post(reverse('grid_crud'),
                         {'oper': 'add', 'name': 'Vasya'})

        count = Item.objects.filter(name=name).count()
        self.assertEqual(1, count)

    def test_delete_item_in_grid(self):
        count = Item.objects.filter(id="1").count()
        self.assertEqual(1, count)

        self.client.post(reverse('grid_crud'), {'oper': 'del', 'id': '1'})

        count = Item.objects.filter(id=1).count()
        self.assertEqual(0, count)

    def test_edit_item_in_grid(self):
        name = "Anastasiia"
        new_name = "NeAnastasiia"

        items = Item.objects.filter(name=name)
        self.assertEqual(1, len(items))
        count = Item.objects.filter(name=new_name).count()
        self.assertEqual(0, count)

        self.client.post(reverse('grid_crud'),
                         {'oper': 'edit', "id": items[0].id, 'name': new_name})

        count = Item.objects.filter(name=name).count()
        self.assertEqual(0, count)
        count = Item.objects.filter(name=new_name).count()
        self.assertEqual(1, count)
