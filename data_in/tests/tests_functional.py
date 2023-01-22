from django.test import TestCase

from ..models import DataSource, DataImport

class FunctionalTests(TestCase):

    def test_can_load_data_from_a_data_source(self):
        # A developer wants to maintain a database of books sourced from a
        # public API. In his Django project, he initiates a data source for
        # said API.
        datasource = DataSource('https://fakerapi.it/api/v1/books?_quantity=2')

        # In a Django view, he tests the data source...
        datasource.test()

        # ...and confirms it can load data.
        test_data_import = DataImport.objects.latest('id')
        self.assertTrue(test_data_import.success)

        # He creates a transform map to map the imported data to his Book model.
        book_transform_map = TransformMap(
            datasource=datasource,
            target=Book,
            map={
                'title': 'title',
                'author': 'author',
                'genre': 'genre',
            }
        )

        # He then tests the transform map and confirms it successfully maps the
        # imported data into the Book model.
        book_transform_map.test()
        book = Book.objects.latest('id')
        self.assertIsNotNone(book.title)
        self.assertIsNotNone(book.author)
        self.assertIsNotNone(book.genre)

        # Finally, he schedules the data source to load once weekly.
        ScheduledImport(
            datasource=datasource,
            transform_map=book_transform_map,
            cadence='weekly',
            day='Saturday',
            time='00:00',
        ).save()

        # At the scheduled date and time, the data source successfully imports
        # data into the Book model
        self.assertGreater(Book.objects.count(), 1)
