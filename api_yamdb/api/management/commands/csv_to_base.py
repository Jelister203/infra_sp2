import csv
import pathlib
from typing import List

from django.core.management import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


def path_become(file_name: str) -> pathlib:
    return pathlib.Path(BASE_DIR, 'static/data', file_name)


class Command(BaseCommand):

    files_to_models = (
        ('category.csv', Category),
        ('genre.csv', Genre),
        ('titles.csv', Title),
        ('genre_title.csv', GenreTitle),
        ('users.csv', User),
        ('review.csv', Review),
        ('comments.csv', Comment),
    )  # order is really important!

    def check_files(self) -> None:
        """
        Folder presence check.

        Сheck for each file in the tuple `files_to_models`.
        Returns:
           None.

        Raises:
            FileNotFoundError: Файл не найден.
        """

        for file_name, _ in self.files_to_models:
            if not path_become(file_name).is_file():
                raise FileNotFoundError(f'{file_name} not exist')

    def to_base(self):
        """
        Transfer data from csv files in the `static/data` directory
        to the database. The names of the columns in the files and fields
        in the corresponding models must match.
        Returns:
            None.
        """
        for file_name, model in self.files_to_models:
            file: pathlib = path_become(file_name)
            date_list = []
            with open(file, 'r', encoding='utf8') as csv_file:
                reader = csv.reader(csv_file, delimiter=',', quotechar='"')
                category_idp: int = 0
                author_idp: int = 0
                for num, row in enumerate(reader):
                    if num == 0:
                        header: List[str] = row
                        continue
                    for idp, param in enumerate(header):
                        if param == 'category':
                            category_idp = idp
                        elif param == 'author':
                            author_idp = idp
                    if category_idp:
                        row[category_idp] = Category.objects.get(
                            id=row[category_idp],
                        )
                    if author_idp:
                        row[author_idp] = User.objects.get(id=row[author_idp])

                    new_date = model(
                        **{key: value for key, value in zip(header, row)},
                    )
                    date_list.append(new_date)
                model.objects.bulk_create(date_list, ignore_conflicts=True)

    def handle(self, *args, **options) -> None:
        """
        Handler for the management command `csv_to_base`.

        Args:
            *args: not used.
            **options: not used.

        Returns:
            None.
        """
        del args, options
        self.check_files()
        self.to_base()
