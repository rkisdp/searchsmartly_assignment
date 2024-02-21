from django.test import TestCase
from django.core.management import call_command
from data_loader.models import PointOfInterest
import os


class DataLoaderTestCase(TestCase):

    def setUp(self):
        self.test_csv_file = 'test_data.csv'
        self.test_json_file = 'test_data.json'
        self.test_xml_file = 'test_data.xml'
        self.invalid_file = 'invalid_file.txt'

        with open(self.test_csv_file, 'w') as f:
            f.write("poi_name,poi_id,poi_category,poi_ratings,poi_latitude,poi_longitude\n")
            f.write("Test POI,1,Test Category,4.5,40.7128,-74.0060\n")

        with open(self.test_json_file, 'w') as f:
            f.write(
                '[{"name": "Test POI", "id": 1, "category": "Test Category", "ratings": 4.5, "description": "Test description", "coordinates": {"latitude": 40.7128, "longitude": -74.0060}}]')

        with open(self.test_xml_file, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<root>\n')
            f.write('<point_of_interest>\n')
            f.write('<pname>Test POI</pname>\n')
            f.write('<pid>1</pid>\n')
            f.write('<pcategory>Test Category</pcategory>\n')
            f.write('<pratings>4.5</pratings>\n')
            f.write('<platitude>40.7128</platitude>\n')
            f.write('<plongitude>-74.0060</plongitude>\n')
            f.write('</point_of_interest>\n')
            f.write('</root>\n')

        with open(self.invalid_file, 'w') as f:
            f.write("poi_name,poi_id,poi_category,poi_ratings,poi_latitude,poi_longitude\n")
            f.write("Test POI,1,Test Category,4.5,40.7128,-74.0060\n")


    def tearDown(self):
        os.remove(self.test_csv_file)
        os.remove(self.test_json_file)
        os.remove(self.test_xml_file)
        os.remove(self.invalid_file)

    def test_csv_import(self):
        call_command('load_data', self.test_csv_file)
        poi = PointOfInterest.objects.get(external_id=1)
        self.assertEqual(poi.name, 'Test POI')
        self.assertEqual(poi.category, 'Test Category')
        self.assertEqual(poi.average_rating, 4.5)

    def test_json_import(self):
        call_command('load_data', self.test_json_file)
        poi = PointOfInterest.objects.get(external_id=1)
        self.assertEqual(poi.name, 'Test POI')
        self.assertEqual(poi.category, 'Test Category')
        self.assertEqual(poi.average_rating, 4.5)

    def test_xml_import(self):
        call_command('load_data', self.test_xml_file)
        poi = PointOfInterest.objects.get(external_id=1)
        self.assertEqual(poi.name, 'Test POI')
        self.assertEqual(poi.category, 'Test Category')
        self.assertEqual(poi.average_rating, 4.5)

    def test_file_not_found(self):
        with self.assertRaisesRegex(Exception, "File not found"):
            call_command('load_data', 'non_existent_file.csv')

    def test_invalid_file_format(self):
        with self.assertRaisesRegex(Exception, "Unsupported file format"):
            call_command('load_data', 'invalid_file.txt')
