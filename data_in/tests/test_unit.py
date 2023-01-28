from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ..models import DataSource, DataImport, TransformMap

from tests.models import Book


class DataSourceTests(TestCase):

    def test_creates_data_import_record_on_test(self):
        # Create data source
        datasource = DataSource('https://fakerapi.it/api/v1/books?_quantity=2')

        # There should be no data import records
        self.assertEqual(DataImport.objects.count(), 0)

        # Test data source import
        datasource.test()

        # There should now be 1 data import record
        self.assertEqual(DataImport.objects.count(), 1)

class TransformMapTests(TestCase):

    def test_creates_record_for_target_object(self):
        # Create data source
        datasource = DataSource('https://fakerapi.it/api/v1/books?_quantity=2')

        # Create transform map
        book_transform_map = TransformMap(
            datasource=datasource,
            target=ContentType.objects.get(app_label='tests', model='book'),
            field_map={
                'title': 'title',
                'author': 'author',
                'genre': 'genre',
            }
        )

        # There should be no Book records
        self.assertEqual(Book.objects.count(), 0)

        # Test the transform map
        book_transform_map.test()

        # There should be a new Book record
        self.assertEqual(Book.objects.count(), 1)


class ScheduledImportTests(TestCase):

    def test_activate_creates_celery_task(self):
        # Create a data source

        # Create a transform map for the data source

        # Schedule an import for the data source

        # Confirm that Celery has a pending task for the data import
        self.fail()
