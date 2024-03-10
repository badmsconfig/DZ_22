# blogapp/management/commands/import_data.py

import os
import pandas as pd
from django.core.management.base import BaseCommand
from blogapp.models import Category  # Импортируйте вашу модель

class Command(BaseCommand):
    help = 'Import data from kat.xlsx to SQLite database'

    def handle(self, *args, **options):
        # Получите путь к файлу kat.xlsx
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kat.xlsx')

        # Прочитайте данные из Excel
        df = pd.read_excel(file_path)

        # Итерируйтесь по строкам и добавьте их в базу данных
        for index, row in df.iterrows():
            Category.objects.create(
                Category=row['Category'],  # Замените на ваши поля
                # Фильмы=row['Фильмы'],
                # ...
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
