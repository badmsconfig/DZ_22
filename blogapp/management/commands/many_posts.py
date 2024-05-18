from django.core.management.base import BaseCommand
from blogapp.models import Post
from usersapp.models import BlogUser
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Create 100 random posts for existing users'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = BlogUser.objects.all()

        if len(users) < 1:
            self.stdout.write(self.style.ERROR('No existing users found. Please create users first.'))
            return

        for _ in range(100):
            # Выбираем рандомного пользователя
            user = random.choice(users)
            # Создаем пост с рандомными данными
            post = Post.objects.create(
                name=fake.sentence(),
                text=fake.paragraph(),
                category=None,  # Здесь нужно указать категорию, если требуется
                user=user
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created post "{post.name}" for user "{user.username}"'))

