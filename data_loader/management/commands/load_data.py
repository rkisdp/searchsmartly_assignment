from django.core.management.base import BaseCommand, CommandError
from data_loader.models import PointOfInterest
import csv
import json
import xml.etree.ElementTree as ET
import os
import requests


class Command(BaseCommand):
    help = 'Loading Points of Interest (PoI) data from a file or files into our database'

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_path in options['files']:
            file_path = self.get_file(file_path)
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
        for poi_element in root.findall('DATA_RECORD'):
            poi_data = self.extract_poi_data_xml(poi_element)
            self.save_poi(poi_data)

    def extract_poi_data_csv(self, data):
        ratings = list(map(float, data['poi_ratings'].strip('{}').split(",")))
        average_rating = sum(ratings) / len(ratings)
        poi_data = {
            'name': data['poi_name'],
            'external_id': data['poi_id'],
            'category': data['poi_category'],
            'average_rating': average_rating,
            'latitude': data['poi_latitude'],
            'longitude': data['poi_longitude'],
        }
        return poi_data

    def extract_poi_data_json(self, data):
        average_rating = sum(data["ratings"]) / len(data["ratings"])
        poi_data = {
            'name': data['name'],
            'external_id': data['id'],
            'category': data['category'],
            'description': data['description'],
            'latitude': data['coordinates']['latitude'],
            'longitude': data['coordinates']['longitude'],
            'average_rating': average_rating,
        }
        return poi_data

    def extract_poi_data_xml(self, element):
        ratings = element.find('pratings').text
        ratings = [float(rating) for rating in ratings.split(',')]
        average_ratings = sum(ratings)/len(ratings)
        poi_data = {
            'name': element.find('pname').text,
            'external_id': element.find('pid').text,
            'latitude': element.find('platitude').text,
            'longitude': element.find('plongitude').text,
            'category': element.find('pcategory').text,
            'average_rating': average_ratings
        }
        return poi_data

    def get_file(self, file):
        if file.startswith('http://') or file.startswith('https://'):
            response = requests.get(file)
            if response.status_code == 200:
                filename = file.split('/')[-1]
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return filename
            else:
                raise CommandError("Failed to download file from the provided link.")
        elif os.path.exists(file):
            return file
        else:
            raise CommandError(f"File not found: {file}")

    def save_poi(self, poi_data):
        obj = PointOfInterest()
        obj.name = poi_data['name']
        obj.external_id = poi_data['external_id']
        obj.category = poi_data['category']
        obj.description = poi_data.get('description')
        obj.latitude = poi_data['latitude']
        obj.longitude = poi_data['longitude']
        obj.average_rating = poi_data['average_rating']
        obj.save()
        self.stdout.write(self.style.SUCCESS(f'external_id: {poi_data['external_id']} successfully saved'))
        return True
