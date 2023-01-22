from django.test import TestCase

from ..models import DataSource, DataImport


class DataSourceTests(TestCase):

    def test_creates_data_import_record_on_test(self):
        # There should be no data import records
        self.assertEqual(DataImport.objects.count(), 0)

        # Create data source
        datasource = DataSource('https://fakerapi.it/api/v1/books?_quantity=2')

        # Test data source import
        datasource.test()

        # There should now be 1 data import record
        self.assertEqual(DataImport.objects.count(), 1)
