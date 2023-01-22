from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from freezegun import freeze_time

from ..models import DataSource, DataImport, TransformMap, ScheduledImport

from tests.models import Book


class FunctionalTests(TestCase):

    @freeze_time("2023-01-23", as_kwarg='frozen_time')
    def test_loads_data_from_a_data_source(self, frozen_time):
        # A developer wants to maintain a database of books sourced from a
        # public API. In his Django project, he initiates a data source for
        # said API.
        datasource = DataSource(url='https://fakerapi.it/api/v1/books?_quantity=2')
        datasource.full_clean()
        datasource.save()

        # In a Django view, he tests the data source...
        datasource.test()

        # ...and confirms it can load data.
        test_data_import = DataImport.objects.latest('id')
        self.assertTrue(test_data_import.success)

        # He creates a transform map to map the imported data to his Book model.
        book_transform_map = TransformMap(
            datasource=datasource,
            target=ContentType.objects.get(app_label='tests', model='book'),
            field_map={
                'title': 'title',
                'author': 'author',
                'genre': 'genre',
            }
        )
        book_transform_map.full_clean()
        book_transform_map.save()

        # He then tests the transform map and confirms it successfully maps the
        # imported data into the Book model.
        book_transform_map.test()
        book = Book.objects.latest('id')
        self.assertIsNotNone(book.title)
        self.assertIsNotNone(book.author)
        self.assertIsNotNone(book.genre)

        # Finally, he schedules the data source to load once weekly.
        scheduled_import = ScheduledImport(
            transform_map=book_transform_map,
            cadence='W',
            day=6,
            time='00:00',
        )
        scheduled_import.full_clean()
        scheduled_import.save()

        # Time passes, past the date the scheduled import is secheduled to run.
        frozen_time.move_to("2023-01-29")

        # At the scheduled date and time, the data source successfully imports
        # data into the Book model
        self.assertGreater(Book.objects.count(), 1)
