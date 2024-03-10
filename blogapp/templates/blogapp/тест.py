from blogapp.models import Category

categories = Category.objects.all()
for category in categories:
    print(f"Category ID: {category.id}, Name: {category.name}")