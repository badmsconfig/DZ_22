from django.test import TestCase
from .models import Post, Category
from usersapp.models import BlogUser
# faker - простые данные, например имя
from faker import Faker
# FactoryBoy - данные для конкретной модели django
# mixer - полностью создать fake модель
from mixer.backend.django import mixer
from django.test import Client




# Create your tests here.
class PostTestCase(TestCase):

    def setUp(self):
        faker = Faker()
        category = Category.objects.create(name='test_category')
        user = BlogUser.objects.create_user(username='test_user', email='test@test.com', password='max1234567')
        self.post = Post.objects.create(name='test_post', text='some', user=user, category=category)

        self.post_str = Post.objects.create(name='test_post_str', text='some', user=user, category=category)
    def test_has_image(self):
        self.assertFalse(self.post.has_image())

    def test_some_method(self):
        post = Post.objects.get(name='test_post')
        self.assertFalse(post.some_method() == 'some method')

    def test_str(self):
        self.assertEquals(str(self.post_str), 'test_post_str, category: test_category')

class PostTestCaseFake(TestCase):

    def setUp(self):
        faker = Faker()
        category = Category.objects.create(name=faker.name())
        user = BlogUser.objects.create_user(username=faker.name(), email='test@test.com', password='max1234567')
        self.post = Post.objects.create(name=faker.name(), text='some', user=user, category=category)

        print(self.post.name)
        print(category.name)

        category = Category.objects.create(name='test_category')
        self.post_str = Post.objects.create(name='test_post_str', text=faker.name(), user=user, category=category)
    def test_has_image(self):
        self.assertFalse(self.post.has_image())

    def test_some_method(self):
        self.assertFalse(self.post.some_method() == 'some method')

    def test_str(self):
        self.assertEquals(str(self.post_str), 'test_post_str, category: test_category')

class PostTestCaseMixer(TestCase):
    def setUp(self):
        # Создаем категорию
        category = mixer.blend(Category, name='test_category')
        # Создаем пользователя
        user = BlogUser.objects.create_user(username='leo', email='test@test.com', password='max1234567')
        # Создаем отдельный пост для использования в тесте test_str
        self.post_str = Post.objects.create(name='test_post_str', text='some', user=user, category=category)

        # Создаем пост, указывая пользователя и категорию
        self.post = mixer.blend(Post, user=user, category=category, image='test_image.jpg')

        print('mixer-name:', self.post.name)
        print('mixer-category', self.post.category)
        print('mixer-category-type', type(self.post.category))
        print('mixer-user-email', self.post.user.email)

        # Хороший вариант
        # category = mixer.blend(Category, name='test_category')
        # self.post_str = mixer.blend(Post, name='test_post_str', category=category)

        # Короткая запись
        # self.post_str = mixer.blend(Post, name='test_post_str', category__name='test_category')

    def test_has_image(self):
        self.assertIsNotNone(self.post.image)
        #self.assertFalse(self.post.has_image())
        #self.assertTrue(self.post.has_image())  # Проверяем наличие изображения

    def test_some_method(self):
        self.assertFalse(self.post.some_method() == 'some method')

    def test_str(self):
        self.assertEqual(str(self.post_str), 'test_post_str, category: test_category')


# class PostTestCaseMixer(TestCase):
#     def setUp(self):
#         # Создаем категорию
#         category = mixer.blend(Category, name='test_category')
#         # Создаем пользователя
#         user = BlogUser.objects.create_user(username='leo', email='test@test.com', password='max1234567')
#         # Создаем отдельный пост для использования в тесте test_str
#         self.post_str = Post.objects.create(name='test_post_str', text='some', user=user, category=category)
#
#         # Создаем пост, указывая пользователя и категорию
#         self.post = mixer.blend(Post, user=user, category=category, image='test_image.jpg')
#
#         print('mixer-name:', self.post.name)
#         print('mixer-category', self.post.category)
#         print('mixer-category-type', type(self.post.category))
#         print('mixer-user-email', self.post.user.email)
#
#         # Хороший вариант
#
#     def test_has_image(self):
#         #self.assertFalse(self.post.has_image())
#         self.assertTrue(self.post.has_image())  # Проверяем наличие изображения
#
#     def test_some_method(self):
#         self.assertFalse(self.post.some_method() == 'some method')
#
#     def test_str(self):
#         self.assertEqual(str(self.post_str), 'test_post_str, category: test_category')


# class PostTestCaseMixer(TestCase):
#
#     def setUp(self):
#         self.post = mixer.blend(Post)
#
#         # print('mixer-name:', self.post.name)
#         # print('mixer-category', self.post.category)
#         # print('mixer-category-type', type(self.post.category))
#         # print('mixer-user-email', self.post.user.email)
#         # Как создать картинку с mixer?
#
#         # Хороший вариант
#         # category = mixer.blend(Category, name='test_category')
#         # self.post_str = mixer.blend(Post, name='test_post_str', category=category)
#
#         # Короткая запись
#         self.post_str = mixer.blend(Post, name='test_post_str', category__name='test_category')
#
#     def test_has_image(self):
#         self.assertFalse(self.post.has_image())
#
#     def test_some_method(self):
#         self.assertFalse(self.post.some_method() == 'some method')
#
#     def test_str(self):
#         self.assertEqual(str(self.post_str), 'test_post_str, category: test_category')
#
#         zzzzzzzzz
#         zzzzzzzzz



class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fake = Faker()

    def test_statuses(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Что мы можем проверить
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        # post зарос
        response = self.client.post('/contact/',
                                    {'name': self.fake.name(), 'message': self.fake.text(),
                                     'email': self.fake.email()})

        self.assertEqual(response.status_code, 302)

        # Какие данные передаются в контексте
        response = self.client.get('/')
        self.assertTrue('posts' in response.context)

    def test_login_required(self):
        BlogUser.objects.create_user(username='test_user', email='test@test.com', password='leo1234567')
        # Он не вошел
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 302)

        # Логиним
        self.client.login(username='test_user', password='leo1234567')

        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)