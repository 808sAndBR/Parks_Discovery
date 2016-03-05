import csv
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from parks_discovery.models import Park


class Command(BaseCommand):
    help = 'Ingests Park CSV content to create Park models.'

    def add_arguments(self, parser):
        parser.add_argument('--filepath')

    def handle(self, *args, **options):
        filepath = options['filepath']
        with open(filepath, 'r') as park_file:
            reader = csv.DictReader(park_file)
            for row in reader:
                park, created = Park.objects.get_or_create(park_id=int(row['ParkID']), 
                    name=row['ParkName'].title(), neighborhood=row['neighborhood'], 
                    psa_manager=row['PSAManager'], zipcode=row['Zipcode'],
                    park_service_area=row['ParkServiceArea'], phone_number=row['Number'],
                    park_type=row['ParkType'], acreage=float(row['Acreage']),
                    email=row['email'], address=row['Location 1'], size=row['size']
                )
                if created:
                    if row['SupDist'] != 'NA':
                        park.district = row['SupDist']
                        park.save()
                    if row['Lat'] != 'NA' and row['Long'] != 'NA':
                        park.latitude = Decimal(row['Lat'])
                        park.longitude = Decimal(row['Long'])
                        park.save()

                    self.stdout.write(self.style.SUCCESS('Successfully created park: "%s"' % park.name))
                else:
                    self.stdout.write(self.style.SUCCESS('Park already exists: "%s"' % park.name))
