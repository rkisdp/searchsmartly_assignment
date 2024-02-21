from django.core.management.base import BaseCommand, CommandError
from django.db import OperationalError
from data_loader.models import PointOfInterest
import csv
import json
import xml.etree.ElementTree as ET
import os


class Command(BaseCommand):
    help = 'Loading Points of Interest (PoI) data from a file or files into our database'

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_path in options['files']:
            if not os.path.exists(file_path):
                raise CommandError(f"File not found: {file_path}")
            file_extension = file_path.split('.')[-1]
            if file_extension == 'csv':
                self.import_pois_from_csv(file_path)
            elif file_extension == 'json':
                self.import_pois_from_json(file_path)
            elif file_extension == 'xml':
                self.import_pois_from_xml(file_path)
            else:
                raise CommandError(f'Unsupported file format: {file_extension}')

    def import_pois_from_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                poi_data = self.extract_poi_data_csv(row)
                self.save_poi(poi_data)

    def import_pois_from_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for entry in data:
                poi_data = self.extract_poi_data_json(entry)
                self.save_poi(poi_data)

    def import_pois_from_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        for poi_element in root.findall('point_of_interest'):
            poi_data = self.extract_poi_data_xml(poi_element)
            self.save_poi(poi_data)

    def extract_poi_data_csv(self, data):
        poi_data = {
            'name': data['poi_name'],
            'external_id': data['poi_id'],
            'category': data['poi_category'],
            'average_rating': float(data['poi_ratings']),
            'latitude': data['poi_latitude'],
            'longitude': data['poi_longitude'],
        }
        return poi_data

    def extract_poi_data_json(self, data):
        poi_data = {
            'name': data['name'],
            'external_id': data['id'],
            'category': data['category'],
            'description': data['description'],
            'latitude': data['coordinates']['latitude'],
            'longitude': data['coordinates']['longitude'],
            'average_rating': float(data['ratings'])
        }
        return poi_data

    def extract_poi_data_xml(self, element):
        poi_data = {
            'name': element.find('pname').text,
            'external_id': element.find('pid').text,
            'latitude': element.find('platitude').text,
            'longitude': element.find('plongitude').text,
            'category': element.find('pcategory').text,
            'average_rating': float(element.find('pratings').text)
        }
        return poi_data

    def save_poi(self, poi_data):
        try:
            obj = PointOfInterest()
            obj.name = poi_data['name']
            obj.external_id = poi_data['external_id']
            obj.category = poi_data['category']
            obj.description = poi_data.get('description')
            obj.latitude = poi_data['latitude']
            obj.longitude = poi_data['longitude']
            obj.average_rating = poi_data['average_rating']
            obj.save()
            self.stdout.write(self.style.SUCCESS(f'data with external_id: {poi_data['external_id']} successfully saved'))
            return True
        except OperationalError:
            self.stdout.write(self.style.ERROR(f'database connection lost'))
            return False
